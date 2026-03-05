"""Model management endpoints."""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.model import Model
from app.schemas.model import ModelCreate, ModelResponse, ModelUpdate

router = APIRouter()


@router.get("", response_model=List[ModelResponse])
async def list_models(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    model_type: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
) -> List[Model]:
    """List all models with optional filtering."""
    query = select(Model)
    if model_type:
        query = query.where(Model.type == model_type)
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{model_id}", response_model=ModelResponse)
async def get_model(
    model_id: str,
    db: AsyncSession = Depends(get_db),
) -> Model:
    """Get a specific model by ID."""
    result = await db.execute(select(Model).where(Model.id == model_id))
    model = result.scalar_one_or_none()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    return model


@router.post("", response_model=ModelResponse, status_code=201)
async def create_model(
    model_in: ModelCreate,
    db: AsyncSession = Depends(get_db),
) -> Model:
    """Create a new model configuration."""
    model = Model(**model_in.model_dump())
    db.add(model)
    await db.commit()
    await db.refresh(model)
    return model


@router.put("/{model_id}", response_model=ModelResponse)
async def update_model(
    model_id: str,
    model_in: ModelUpdate,
    db: AsyncSession = Depends(get_db),
) -> Model:
    """Update a model configuration."""
    result = await db.execute(select(Model).where(Model.id == model_id))
    model = result.scalar_one_or_none()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")

    update_data = model_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(model, field, value)

    await db.commit()
    await db.refresh(model)
    return model


@router.delete("/{model_id}", status_code=204)
async def delete_model(
    model_id: str,
    db: AsyncSession = Depends(get_db),
) -> None:
    """Delete a model configuration."""
    result = await db.execute(select(Model).where(Model.id == model_id))
    model = result.scalar_one_or_none()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    await db.delete(model)
    await db.commit()