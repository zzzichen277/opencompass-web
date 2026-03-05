"""Dataset management endpoints."""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.dataset import Dataset
from app.schemas.dataset import DatasetCreate, DatasetResponse, DatasetUpdate
from app.services.opencompass import opencompass_service

router = APIRouter()


@router.get("", response_model=List[DatasetResponse])
async def list_datasets(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    dataset_type: Optional[str] = None,
    category: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
) -> List[Dataset]:
    """List all datasets with optional filtering."""
    query = select(Dataset)
    if dataset_type:
        query = query.where(Dataset.type == dataset_type)
    if category:
        query = query.where(Dataset.category == category)
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/builtin", response_model=List[DatasetResponse])
async def list_builtin_datasets(
    db: AsyncSession = Depends(get_db),
) -> List[dict]:
    """List all built-in datasets from OpenCompass configurations."""
    # Get from OpenCompass service
    builtin_datasets = opencompass_service.get_builtin_datasets()

    # Also check database for any saved builtin datasets
    result = await db.execute(
        select(Dataset).where(Dataset.type == "builtin")
    )
    db_datasets = result.scalars().all()
    db_dataset_ids = {d.id for d in db_datasets}

    # Combine results
    all_datasets = []
    for ds in builtin_datasets:
        if ds["id"] not in db_dataset_ids:
            all_datasets.append(ds)

    all_datasets.extend([{"id": d.id, "name": d.name, "type": d.type,
                          "category": d.category, "description": d.description,
                          "config_path": d.config_path, "metrics": d.metrics,
                          "sample_count": d.sample_count, "tags": d.tags,
                          "created_at": d.created_at.isoformat() if d.created_at else None}
                         for d in db_datasets])

    return all_datasets


@router.get("/{dataset_id}", response_model=DatasetResponse)
async def get_dataset(
    dataset_id: str,
    db: AsyncSession = Depends(get_db),
) -> Dataset:
    """Get a specific dataset by ID."""
    result = await db.execute(select(Dataset).where(Dataset.id == dataset_id))
    dataset = result.scalar_one_or_none()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return dataset


@router.post("", response_model=DatasetResponse, status_code=201)
async def create_dataset(
    dataset_in: DatasetCreate,
    db: AsyncSession = Depends(get_db),
) -> Dataset:
    """Create a new dataset configuration."""
    dataset = Dataset(**dataset_in.model_dump())
    db.add(dataset)
    await db.commit()
    await db.refresh(dataset)
    return dataset


@router.post("/upload", response_model=DatasetResponse, status_code=201)
async def upload_dataset(
    file: UploadFile = File(...),
    name: str = Query(...),
    category: str = Query(...),
    db: AsyncSession = Depends(get_db),
) -> Dataset:
    """Upload a custom dataset file."""
    # TODO: Implement file upload and parsing logic
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.put("/{dataset_id}", response_model=DatasetResponse)
async def update_dataset(
    dataset_id: str,
    dataset_in: DatasetUpdate,
    db: AsyncSession = Depends(get_db),
) -> Dataset:
    """Update a dataset configuration."""
    result = await db.execute(select(Dataset).where(Dataset.id == dataset_id))
    dataset = result.scalar_one_or_none()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    update_data = dataset_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(dataset, field, value)

    await db.commit()
    await db.refresh(dataset)
    return dataset


@router.delete("/{dataset_id}", status_code=204)
async def delete_dataset(
    dataset_id: str,
    db: AsyncSession = Depends(get_db),
) -> None:
    """Delete a dataset configuration."""
    result = await db.execute(select(Dataset).where(Dataset.id == dataset_id))
    dataset = result.scalar_one_or_none()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    await db.delete(dataset)
    await db.commit()