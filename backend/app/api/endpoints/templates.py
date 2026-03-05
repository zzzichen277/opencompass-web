"""Task template management endpoints."""

from typing import List, Optional
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.template import TaskTemplate
from app.schemas.template import TemplateCreate, TemplateResponse, TemplateUpdate

router = APIRouter()


@router.get("", response_model=List[TemplateResponse])
async def list_templates(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
) -> List[TaskTemplate]:
    """List all task templates."""
    result = await db.execute(
        select(TaskTemplate).order_by(TaskTemplate.created_at.desc()).offset(skip).limit(limit)
    )
    return result.scalars().all()


@router.get("/{template_id}", response_model=TemplateResponse)
async def get_template(
    template_id: str,
    db: AsyncSession = Depends(get_db),
) -> TaskTemplate:
    """Get a specific template by ID."""
    result = await db.execute(
        select(TaskTemplate).where(TaskTemplate.id == template_id)
    )
    template = result.scalar_one_or_none()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return template


@router.post("", response_model=TemplateResponse, status_code=201)
async def create_template(
    template_in: TemplateCreate,
    db: AsyncSession = Depends(get_db),
) -> TaskTemplate:
    """Create a new task template."""
    template = TaskTemplate(**template_in.model_dump())
    db.add(template)
    await db.commit()
    await db.refresh(template)
    return template


@router.put("/{template_id}", response_model=TemplateResponse)
async def update_template(
    template_id: str,
    template_in: TemplateUpdate,
    db: AsyncSession = Depends(get_db),
) -> TaskTemplate:
    """Update a task template."""
    result = await db.execute(
        select(TaskTemplate).where(TaskTemplate.id == template_id)
    )
    template = result.scalar_one_or_none()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")

    update_data = template_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(template, field, value)

    await db.commit()
    await db.refresh(template)
    return template


@router.delete("/{template_id}", status_code=204)
async def delete_template(
    template_id: str,
    db: AsyncSession = Depends(get_db),
) -> None:
    """Delete a task template."""
    result = await db.execute(
        select(TaskTemplate).where(TaskTemplate.id == template_id)
    )
    template = result.scalar_one_or_none()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    await db.delete(template)
    await db.commit()