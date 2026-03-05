"""Background task executor for evaluation jobs."""

import asyncio
from datetime import datetime
from typing import Dict, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import async_session_maker
from app.models.task import EvaluationTask
from app.models.result import EvaluationResult
from app.models.log import EvaluationLog
from app.services.opencompass import opencompass_service


class TaskExecutor:
    """Executor for running evaluation tasks in background."""

    def __init__(self):
        """Initialize task executor."""
        self.running_tasks: Dict[str, asyncio.Task] = {}
        self.progress_callbacks = []
        self.log_callbacks = []

    def register_progress_callback(self, callback):
        """Register a callback for progress updates."""
        self.progress_callbacks.append(callback)

    def register_log_callback(self, callback):
        """Register a callback for log updates."""
        self.log_callbacks.append(callback)

    async def _notify_progress(self, task_id: str, progress: float, **kwargs):
        """Notify all registered progress callbacks."""
        for callback in self.progress_callbacks:
            try:
                await callback(task_id, progress, **kwargs)
            except Exception:
                pass

    async def _notify_log(self, task_id: str, level: str, message: str):
        """Notify all registered log callbacks."""
        for callback in self.log_callbacks:
            try:
                await callback(task_id, level, message)
            except Exception:
                pass

    async def start_task(self, task_id: str) -> bool:
        """Start a task execution.

        Args:
            task_id: ID of the task to start

        Returns:
            True if task started successfully
        """
        if task_id in self.running_tasks:
            return False

        async with async_session_maker() as db:
            result = await db.execute(
                select(EvaluationTask).where(EvaluationTask.id == task_id)
            )
            task = result.scalar_one_or_none()

            if not task:
                return False

            if task.status not in ["pending", "failed"]:
                return False

            # Update task status
            task.status = "running"
            task.started_at = datetime.utcnow()
            await db.commit()

        # Start background execution
        async_task = asyncio.create_task(self._execute_task(task_id))
        self.running_tasks[task_id] = async_task

        return True

    async def stop_task(self, task_id: str) -> bool:
        """Stop a running task.

        Args:
            task_id: ID of the task to stop

        Returns:
            True if task stopped successfully
        """
        if task_id not in self.running_tasks:
            return False

        async_task = self.running_tasks[task_id]
        async_task.cancel()

        try:
            await async_task
        except asyncio.CancelledError:
            pass

        del self.running_tasks[task_id]

        # Update task status
        async with async_session_maker() as db:
            result = await db.execute(
                select(EvaluationTask).where(EvaluationTask.id == task_id)
            )
            task = result.scalar_one_or_none()
            if task:
                task.status = "cancelled"
                task.completed_at = datetime.utcnow()
                await db.commit()

        return True

    async def _execute_task(self, task_id: str):
        """Execute the evaluation task.

        Args:
            task_id: ID of the task to execute
        """
        try:
            async with async_session_maker() as db:
                result = await db.execute(
                    select(EvaluationTask).where(EvaluationTask.id == task_id)
                )
                task = result.scalar_one_or_none()

                if not task:
                    return

                config = task.config
                models = config.get("models", [])
                datasets = config.get("datasets", [])
                accelerator = config.get("accelerator", "huggingface")

                # Generate OpenCompass config
                config_path = opencompass_service.generate_eval_config(
                    task_name=task.name,
                    models=[{"type": "huggingface", "path": m} for m in models],
                    datasets=datasets,
                    accelerator=accelerator,
                )

                # Log task start
                await self._save_log(db, task_id, "info", f"Starting evaluation task: {task.name}")
                await self._notify_log(task_id, "info", f"Starting evaluation task: {task.name}")

                # Run evaluation
                eval_results = await opencompass_service.run_evaluation(
                    config_path=config_path,
                    task_id=task_id,
                    progress_callback=self._progress_callback,
                    log_callback=self._log_callback,
                )

                if eval_results["status"] == "completed":
                    # Save results
                    await self._save_results(db, task_id, eval_results)

                    task.status = "completed"
                    task.progress = 100.0
                    task.completed_at = datetime.utcnow()
                    await db.commit()

                    await self._notify_progress(task_id, 100.0, status="completed")
                    await self._save_log(db, task_id, "info", "Task completed successfully")

                else:
                    task.status = "failed"
                    task.error_message = "; ".join(eval_results.get("errors", ["Unknown error"]))
                    task.completed_at = datetime.utcnow()
                    await db.commit()

                    await self._save_log(db, task_id, "error", task.error_message)
                    await self._notify_log(task_id, "error", task.error_message)

        except asyncio.CancelledError:
            async with async_session_maker() as db:
                result = await db.execute(
                    select(EvaluationTask).where(EvaluationTask.id == task_id)
                )
                task = result.scalar_one_or_none()
                if task:
                    task.status = "cancelled"
                    task.completed_at = datetime.utcnow()
                    await db.commit()

        except Exception as e:
            async with async_session_maker() as db:
                result = await db.execute(
                    select(EvaluationTask).where(EvaluationTask.id == task_id)
                )
                task = result.scalar_one_or_none()
                if task:
                    task.status = "failed"
                    task.error_message = str(e)
                    task.completed_at = datetime.utcnow()
                    await db.commit()

                await self._save_log(db, task_id, "error", str(e))
                await self._notify_log(task_id, "error", str(e))

        finally:
            if task_id in self.running_tasks:
                del self.running_tasks[task_id]

    async def _progress_callback(self, task_id: str, progress: float):
        """Internal progress callback."""
        async with async_session_maker() as db:
            result = await db.execute(
                select(EvaluationTask).where(EvaluationTask.id == task_id)
            )
            task = result.scalar_one_or_none()
            if task:
                task.progress = progress
                await db.commit()

        await self._notify_progress(task_id, progress)

    async def _log_callback(self, task_id: str, level: str, message: str):
        """Internal log callback."""
        async with async_session_maker() as db:
            await self._save_log(db, task_id, level, message)

        await self._notify_log(task_id, level, message)

    async def _save_log(self, db: AsyncSession, task_id: str, level: str, message: str):
        """Save log entry to database."""
        log = EvaluationLog(
            task_id=task_id,
            level=level,
            message=message,
        )
        db.add(log)
        await db.commit()

    async def _save_results(self, db: AsyncSession, task_id: str, results: Dict):
        """Save evaluation results to database."""
        config = results.get("config", {})
        models = config.get("models", [])
        datasets = config.get("datasets", [])
        scores = results.get("scores", {})

        for model_id in models:
            for dataset_id in datasets:
                result = EvaluationResult(
                    task_id=task_id,
                    model_id=model_id,
                    dataset_id=dataset_id,
                    overall_score=scores.get(f"{model_id}_{dataset_id}", 0.0),
                    metrics=scores,
                )
                db.add(result)

        await db.commit()


# Singleton instance
task_executor = TaskExecutor()