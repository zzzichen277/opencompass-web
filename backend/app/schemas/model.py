"""Pydantic schemas for Model endpoints."""

from datetime import datetime
from typing import Optional, List, Dict, Any

from pydantic import BaseModel, Field


class ModelBase(BaseModel):
    """Base model schema."""

    name: str = Field(..., description="Model name")
    type: str = Field(..., description="Model type: huggingface, api, custom")
    path: Optional[str] = Field(None, description="Model path for HuggingFace models")
    api_config: Optional[Dict[str, Any]] = Field(None, description="API configuration for API models")
    parameters: Optional[Dict[str, Any]] = Field(None, description="Model parameters")
    tags: Optional[List[str]] = Field(None, description="Model tags")


class ModelCreate(ModelBase):
    """Schema for creating a model."""

    pass


class ModelUpdate(BaseModel):
    """Schema for updating a model."""

    name: Optional[str] = None
    type: Optional[str] = None
    path: Optional[str] = None
    api_config: Optional[Dict[str, Any]] = None
    parameters: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None


class ModelResponse(ModelBase):
    """Schema for model response."""

    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True