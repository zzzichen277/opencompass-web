"""Evaluation log database model."""

import uuid
from datetime import datetime

from sqlalchemy import String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class EvaluationLog(Base):
    """Evaluation log for tracking execution progress."""

    __tablename__ = "evaluation_logs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    task_id: Mapped[str] = mapped_column(String(36), index=True, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    level: Mapped[str] = mapped_column(String(20), default="info")  # debug, info, warning, error
    message: Mapped[str] = mapped_column(Text, nullable=False)