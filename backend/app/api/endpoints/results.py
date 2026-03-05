"""Evaluation result endpoints."""

from typing import List, Optional
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.result import EvaluationResult
from app.models.task import EvaluationTask
from app.models.dataset import Dataset
from app.models.model import Model
from app.schemas.result import ResultResponse, ResultDetail, LeaderboardEntry
from app.services.report import report_service

router = APIRouter()


@router.get("/task/{task_id}", response_model=List[ResultResponse])
async def get_task_results(
    task_id: str,
    db: AsyncSession = Depends(get_db),
) -> List[EvaluationResult]:
    """Get all results for a specific task."""
    result = await db.execute(
        select(EvaluationResult).where(EvaluationResult.task_id == task_id)
    )
    return result.scalars().all()


@router.get("/leaderboard", response_model=List[LeaderboardEntry])
async def get_leaderboard(
    dataset: Optional[str] = None,
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
) -> List[dict]:
    """Get model leaderboard rankings."""
    # TODO: Implement leaderboard calculation
    return []


@router.get("/{result_id}", response_model=ResultResponse)
async def get_result(
    result_id: str,
    db: AsyncSession = Depends(get_db),
) -> EvaluationResult:
    """Get a specific evaluation result."""
    result = await db.execute(
        select(EvaluationResult).where(EvaluationResult.id == result_id)
    )
    eval_result = result.scalar_one_or_none()
    if not eval_result:
        raise HTTPException(status_code=404, detail="Result not found")
    return eval_result


@router.get("/{result_id}/details", response_model=ResultDetail)
async def get_result_details(
    result_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Get detailed results for a specific evaluation."""
    # TODO: Implement detailed result retrieval
    result = await db.execute(
        select(EvaluationResult).where(EvaluationResult.id == result_id)
    )
    eval_result = result.scalar_one_or_none()
    if not eval_result:
        raise HTTPException(status_code=404, detail="Result not found")

    return {
        "result_id": result_id,
        "details": [],
        "skip": skip,
        "limit": limit,
    }


@router.get("/task/{task_id}/export")
async def export_task_results(
    task_id: str,
    format: str = Query("json", regex="^(json|excel|html|csv)$"),
    db: AsyncSession = Depends(get_db),
) -> Response:
    """Export evaluation task results in specified format."""
    # Get task info
    task_result = await db.execute(
        select(EvaluationTask).where(EvaluationTask.id == task_id)
    )
    task = task_result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Get results
    results_result = await db.execute(
        select(EvaluationResult).where(EvaluationResult.task_id == task_id)
    )
    results = results_result.scalars().all()

    # Get models and datasets from config
    config = task.config or {}
    model_ids = config.get("models", [])
    dataset_ids = config.get("datasets", [])

    # Get model details
    models = []
    for model_id in model_ids:
        model_result = await db.execute(
            select(Model).where(Model.id == model_id)
        )
        model = model_result.scalar_one_or_none()
        if model:
            models.append({
                "name": model.name,
                "type": model.type,
                "path": model.path,
            })

    # Get dataset details
    datasets = []
    for dataset_id in dataset_ids:
        dataset_result = await db.execute(
            select(Dataset).where(Dataset.id == dataset_id)
        )
        dataset = dataset_result.scalar_one_or_none()
        if dataset:
            datasets.append({
                "name": dataset.name,
                "category": dataset.category,
                "sample_count": dataset.sample_count,
            })

    # Build results data
    results_data = {
        "scores": {r.model_id: {"overall": r.overall_score, "metrics": r.metrics} for r in results}
    }

    # Generate export based on format
    if format == "json":
        import json
        data = {
            "task": {
                "name": task.name,
                "description": task.description,
                "status": task.status,
                "created_at": task.created_at.isoformat() if task.created_at else None,
                "completed_at": task.completed_at.isoformat() if task.completed_at else None,
            },
            "models": models,
            "datasets": datasets,
            "results": results_data,
        }
        return Response(
            content=json.dumps(data, ensure_ascii=False, indent=2),
            media_type="application/json",
            headers={"Content-Disposition": f"attachment; filename=report_{task_id}.json"}
        )

    elif format == "html":
        html_content = report_service.generate_html_report(
            task_name=task.name,
            task_description=task.description,
            results=results_data,
            models=models,
            datasets=datasets,
        )
        return Response(
            content=html_content,
            media_type="text/html",
            headers={"Content-Disposition": f"attachment; filename=report_{task_id}.html"}
        )

    elif format in ["excel", "csv"]:
        data = report_service.generate_excel_data(
            task_name=task.name,
            results=results_data,
            models=models,
            datasets=datasets,
        )
        media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" if format == "excel" else "text/csv"
        ext = "xlsx" if format == "excel" else "csv"
        return Response(
            content=data,
            media_type=media_type,
            headers={"Content-Disposition": f"attachment; filename=report_{task_id}.{ext}"}
        )

    raise HTTPException(status_code=400, detail="Invalid format")