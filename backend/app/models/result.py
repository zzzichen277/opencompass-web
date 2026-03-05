"""Evaluation result database model."""

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import JSON, String, Text, DateTime, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


def generate_uuid() -> str:
    """Generate a UUID string."""
    return str(uuid.uuid4())


class EvaluationResult(Base):
    """Evaluation result storing scores and metrics."""

    __tablename__ = "evaluation_results"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    task_id: Mapped[str] = mapped_column(String(36), ForeignKey("evaluation_tasks.id"), nullable=False, index=True)
    model_id: Mapped[str] = mapped_column(String(36), ForeignKey("models.id"), nullable=False, index=True)
    dataset_id: Mapped[str] = mapped_column(String(36), ForeignKey("datasets.id"), nullable=False, index=True)
    overall_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    metrics: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    summary: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    details_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)