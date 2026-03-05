"""Pydantic schemas for Dataset endpoints."""

from datetime import datetime
from typing import Optional, List, Dict, Any

from pydantic import BaseModel, Field


class DatasetBase(BaseModel):
    """Base dataset schema."""

    name: str = Field(..., description="Dataset name")
    type: str = Field(..., description="Dataset type: builtin, custom")
    category: Optional[str] = Field(None, description="Dataset category: qa, math, code, subjective, reasoning")
    description: Optional[str] = Field(None, description="Dataset description")
    config_path: Optional[str] = Field(None, description="OpenCompass config path")
    custom_data: Optional[Dict[str, Any]] = Field(None, description="Custom data configuration")
    metrics: Optional[List[str]] = Field(None, description="Evaluation metrics")
    sample_count: Optional[int] = Field(None, description="Number of samples")
    tags: Optional[List[str]] = Field(None, description="Dataset tags")


class DatasetCreate(DatasetBase):
    """Schema for creating a dataset."""

    pass


class DatasetUpdate(BaseModel):
    """Schema for updating a dataset."""

    name: Optional[str] = None
    type: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    config_path: Optional[str] = None
    custom_data: Optional[Dict[str, Any]] = None
    metrics: Optional[List[str]] = None
    sample_count: Optional[int] = None
    tags: Optional[List[str]] = None


class DatasetResponse(DatasetBase):
    """Schema for dataset response."""

    id: str
    created_at: datetime

    class Config:
        from_attributes = True