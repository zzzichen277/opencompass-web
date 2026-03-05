"""Dataset configuration database model."""

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import JSON, String, Text, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


def generate_uuid() -> str:
    """Generate a UUID string."""
    return str(uuid.uuid4())


class Dataset(Base):
    """Dataset configuration for evaluation."""

    __tablename__ = "datasets"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    type: Mapped[str] = mapped_column(String(50), nullable=False)  # builtin, custom
    category: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # qa, math, code, subjective, reasoning
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    config_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    custom_data: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    metrics: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    sample_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    tags: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)