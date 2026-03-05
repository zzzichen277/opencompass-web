"""Pydantic schemas for Task endpoints."""

from datetime import datetime
from typing import Optional, List, Dict, Any

from pydantic import BaseModel, Field


class ResourceConfig(BaseModel):
    """Resource configuration for evaluation task."""

    gpu_count: int = Field(1, ge=0, description="Number of GPUs to use")
    max_num_worker: int = Field(1, ge=1, description="Maximum number of workers for data parallel")
    batch_size: Optional[int] = Field(None, description="Batch size")


class EvalConfig(BaseModel):
    """Evaluation configuration."""

    mode: str = Field("gen", description="Evaluation mode: gen or ppl")
    max_out_len: Optional[int] = Field(2048, description="Maximum output length")
    batch_size: Optional[int] = Field(None, description="Batch size")


class TaskConfig(BaseModel):
    """Task configuration schema."""

    models: List[str] = Field(..., description="List of model IDs to evaluate")
    datasets: List[str] = Field(..., description="List of dataset IDs to evaluate")
    accelerator: str = Field("huggingface", description="Accelerator: huggingface, vllm, lmdeploy")
    resources: ResourceConfig = Field(default_factory=ResourceConfig)
    eval_config: EvalConfig = Field(default_factory=EvalConfig)


class TaskBase(BaseModel):
    """Base task schema."""

    name: str = Field(..., description="Task name")
    description: Optional[str] = Field(None, description="Task description")


class TaskCreate(TaskBase):
    """Schema for creating a task."""

    config: TaskConfig


class TaskUpdate(BaseModel):
    """Schema for updating a task."""

    name: Optional[str] = None
    description: Optional[str] = None
    config: Optional[TaskConfig] = None


class TaskResponse(TaskBase):
    """Schema for task response."""

    id: str
    config: Dict[str, Any]
    status: str
    progress: float
    error_message: Optional[str]
    created_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]

    class Config:
        from_attributes = True