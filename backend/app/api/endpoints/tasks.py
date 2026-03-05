"""Evaluation task endpoints."""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.task import EvaluationTask
from app.models.log import EvaluationLog
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate, TaskConfig
from app.tasks.executor import task_executor

router = APIRouter()


@router.get("", response_model=List[TaskResponse])
async def list_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
) -> List[EvaluationTask]:
    """List all evaluation tasks with optional filtering."""
    query = select(EvaluationTask)
    if status:
        query = query.where(EvaluationTask.status == status)
    query = query.order_by(EvaluationTask.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: str,
    db: AsyncSession = Depends(get_db),
) -> EvaluationTask:
    """Get a specific evaluation task by ID."""
    result = await db.execute(
        select(EvaluationTask).where(EvaluationTask.id == task_id)
    )
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post("", response_model=TaskResponse, status_code=201)
async def create_task(
    task_in: TaskCreate,
    db: AsyncSession = Depends(get_db),
) -> EvaluationTask:
    """Create a new evaluation task."""
    task = EvaluationTask(
        name=task_in.name,
        description=task_in.description,
        config=task_in.config.model_dump(),
        status="pending",
    )
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


@router.post("/{task_id}/start", response_model=TaskResponse)
async def start_task(
    task_id: str,
    db: AsyncSession = Depends(get_db),
) -> EvaluationTask:
    """Start an evaluation task."""
    result = await db.execute(
        select(EvaluationTask).where(EvaluationTask.id == task_id)
    )
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.status not in ["pending", "failed"]:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot start task with status: {task.status}",
        )

    # Start task execution
    started = await task_executor.start_task(task_id)
    if not started:
        raise HTTPException(status_code=500, detail="Failed to start task")

    # Refresh to get updated status
    await db.refresh(task)
    return task


@router.post("/{task_id}/stop", response_model=TaskResponse)
async def stop_task(
    task_id: str,
    db: AsyncSession = Depends(get_db),
) -> EvaluationTask:
    """Stop a running evaluation task."""
    result = await db.execute(
        select(EvaluationTask).where(EvaluationTask.id == task_id)
    )
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.status != "running":
        raise HTTPException(
            status_code=400,
            detail=f"Cannot stop task with status: {task.status}",
        )

    # Stop task execution
    stopped = await task_executor.stop_task(task_id)
    if not stopped:
        raise HTTPException(status_code=500, detail="Failed to stop task")

    # Refresh to get updated status
    await db.refresh(task)
    return task


@router.get("/{task_id}/logs")
async def get_task_logs(
    task_id: str,
    offset: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Get logs for a specific task."""
    # Verify task exists
    result = await db.execute(
        select(EvaluationTask).where(EvaluationTask.id == task_id)
    )
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Get logs from database
    logs_result = await db.execute(
        select(EvaluationLog)
        .where(EvaluationLog.task_id == task_id)
        .order_by(EvaluationLog.timestamp.desc())
        .offset(offset)
        .limit(limit)
    )
    logs = logs_result.scalars().all()

    return {
        "task_id": task_id,
        "logs": [
            {
                "timestamp": log.timestamp.isoformat(),
                "level": log.level,
                "message": log.message
            }
            for log in reversed(logs)
        ],
        "offset": offset,
        "limit": limit,
        "total": len(logs)
    }


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: str,
    task_in: TaskUpdate,
    db: AsyncSession = Depends(get_db),
) -> EvaluationTask:
    """Update an evaluation task."""
    result = await db.execute(
        select(EvaluationTask).where(EvaluationTask.id == task_id)
    )
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    update_data = task_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    await db.commit()
    await db.refresh(task)
    return task


@router.delete("/{task_id}", status_code=204)
async def delete_task(
    task_id: str,
    db: AsyncSession = Depends(get_db),
) -> None:
    """Delete an evaluation task."""
    result = await db.execute(
        select(EvaluationTask).where(EvaluationTask.id == task_id)
    )
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.status == "running":
        raise HTTPException(status_code=400, detail="Cannot delete running task")
    await db.delete(task)
    await db.commit()