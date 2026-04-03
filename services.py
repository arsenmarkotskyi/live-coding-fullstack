from __future__ import annotations

from typing import Any, List

from sqlalchemy import func
from sqlalchemy.orm import Session

from models import Alert, AlertEvent, AlertRowOut, Project, ProjectRowOut


class ProjectsController:
    @classmethod
    def list_projects(cls, db: Session) -> List[ProjectRowOut]:
        rows = db.query(Project).order_by(Project.name.asc()).all()
        return [ProjectRowOut.model_validate(p) for p in rows]


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
        alerts_query = (
            db.query(Alert, Project.name, func.count(AlertEvent.id))
            .join(Project, Alert.project_id == Project.id)
            .outerjoin(AlertEvent, Alert.id == AlertEvent.alert_id)
        )
        for field, column in cls._FILTERABLE.items():
            if (value := filters.get(field)) is not None:
                alerts_query = alerts_query.filter(column == value)
        alerts_query = alerts_query.group_by(Alert, Project.name).order_by(
            Alert.created_at.desc(),
            Alert.id.desc(),
        )
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
