"""Pydantic schemas for Result endpoints."""

from datetime import datetime
from typing import Optional, List, Dict, Any

from pydantic import BaseModel, Field


class ResultBase(BaseModel):
    """Base result schema."""

    task_id: str
    model_id: str
    dataset_id: str
    overall_score: Optional[float] = None
    metrics: Optional[Dict[str, Any]] = None
    summary: Optional[Dict[str, Any]] = None


class ResultResponse(ResultBase):
    """Schema for result response."""

    id: str
    details_path: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class ResultDetail(BaseModel):
    """Schema for detailed result."""

    result_id: str
    details: List[Dict[str, Any]]
    skip: int
    limit: int


class LeaderboardEntry(BaseModel):
    """Schema for leaderboard entry."""

    model_id: str
    model_name: str
    dataset_id: str
    dataset_name: str
    score: float
    rank: int
    metrics: Optional[Dict[str, Any]] = None