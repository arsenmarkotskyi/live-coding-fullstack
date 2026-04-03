from pydantic import BaseModel
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class ProjectRowOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class AlertRowOut(BaseModel):
    id: int
    project_id: int
    project_name: str
    title: str
    severity: str
    created_at: str
    events_count: int

    class Config:
        from_attributes = True


class Base(DeclarativeBase):
    pass


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    key: Mapped[str]
    name: Mapped[str]


class Alert(Base):
    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int]
    title: Mapped[str]
    severity: Mapped[str]
    created_at: Mapped[str]


class AlertEvent(Base):
    __tablename__ = "alert_events"

    id: Mapped[int] = mapped_column(primary_key=True)
    alert_id: Mapped[int] = mapped_column(ForeignKey("alerts.id", ondelete="CASCADE"))
    type: Mapped[str]
    payload: Mapped[str | None]
    created_at: Mapped[str]
