from __future__ import annotations

from typing import List

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from dependencies import get_db
from models import AlertRowOut, ProjectRowOut
from services import AlertsController, ProjectsController

app = FastAPI(title="live coding test API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/projects", response_model=List[ProjectRowOut])
def list_projects(db: Session = Depends(get_db)):
    return ProjectsController.list_projects(db)


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
