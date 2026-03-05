"""Pydantic schemas for Template endpoints."""

from datetime import datetime
from typing import Optional, Dict, Any

from pydantic import BaseModel, Field


class TemplateBase(BaseModel):
    """Base template schema."""

    name: str = Field(..., description="Template name")
    description: Optional[str] = Field(None, description="Template description")
    config: Dict[str, Any] = Field(..., description="Task configuration")


class TemplateCreate(TemplateBase):
    """Schema for creating a template."""

    pass


class TemplateUpdate(BaseModel):
    """Schema for updating a template."""

    name: Optional[str] = None
    description: Optional[str] = None
    config: Optional[Dict[str, Any]] = None


class TemplateResponse(TemplateBase):
    """Schema for template response."""

    id: str
    created_at: datetime

    class Config:
        from_attributes = True