from __future__ import annotations

from typing import Any, List

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func
from sqlalchemy.orm import Session

from dependencies import get_db
from models import Alert, AlertEvent, AlertRowOut, Project, ProjectRowOut

app = FastAPI(title="live coding test API")

# PORT = int(os.environ["PORT"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class AlertsController:
    _FILTERABLE: dict[str, Any] = {
        "severity": Alert.severity,
        "project_id": Alert.project_id,
        "title": Alert.title,
        "project_name": Project.name,
    }

    @classmethod
    async def get_alerts(cls, db: Session, filters: dict[str, Any] | None = None) -> List[AlertRowOut]:
        filters = filters or {}
        event_counts_subquery = (
            db.query(
                AlertEvent.alert_id,
                func.count(AlertEvent.id).label("events_count"),
            )
            .group_by(AlertEvent.alert_id)
            .subquery()
        )
        alerts_query = (
            db.query(Alert, Project.name, func.coalesce(event_counts_subquery.c.events_count, 0))
            .join(Project, Alert.project_id == Project.id)
            .outerjoin(event_counts_subquery, Alert.id == event_counts_subquery.c.alert_id)
        )
        for field, column in cls._FILTERABLE.items():
            if (value := filters.get(field)) is not None:
                alerts_query = alerts_query.filter(column == value)
        alerts_query = alerts_query.order_by(Alert.created_at.desc(), Alert.id.desc())
        return [
            AlertRowOut(
                id=alert.id,
                project_id=alert.project_id,
                project_name=project_name,
                title=alert.title,
                severity=alert.severity,
                created_at=alert.created_at,
                events_count=int(events_count),
            )
            for alert, project_name, events_count in alerts_query.all()
        ]


@app.get("/projects", response_model=List[ProjectRowOut])
def list_projects(db: Session = Depends(get_db)):
    rows = db.query(Project).order_by(Project.name.asc()).all()
    return [ProjectRowOut.model_validate(p) for p in rows]


@app.get("/alerts", response_model=List[AlertRowOut])
async def list_alerts(
    db: Session = Depends(get_db),
    severity: str | None = None,
    project_id: int | None = None,
    project_name: str | None = None,
    title: str | None = None,
):
    return await AlertsController.get_alerts(
        db,
        filters={
            "severity": severity,
            "project_id": project_id,
            "project_name": project_name,
            "title": title,
        },
    )
