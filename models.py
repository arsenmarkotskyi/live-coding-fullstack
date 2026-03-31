from typing import Literal

from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class AlertOut(BaseModel):
    id: int
    project: str
    title: str
    severity: Literal["low", "medium", "high"]
    created_at: str
    events_count: int


class Base(DeclarativeBase):
    pass


class Alert(Base):
    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int]
    title: Mapped[str]
    severity: Mapped[str]
    created_at: Mapped[str]

