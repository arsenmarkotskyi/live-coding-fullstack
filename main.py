from __future__ import annotations

import sqlite3
from typing import List

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from dependencies import get_db
from models import AlertRowOut, Alert

app = FastAPI(title="live coding test API")

_DB = None

def DB():
    global _DB
    if _DB is None:
        _DB = sqlite3.connect("db.sqlite")
        _DB.row_factory = sqlite3.Row
    return _DB

# 1.
@app.get("/alerts-first")
def list_alerts_sql():
    cur = DB().cursor()
    rows = cur.execute(
        """
        SELECT id, project_id, title, severity, created_at
        FROM alerts
        ORDER BY created_at DESC, id DESC
        """
    ).fetchall()
    return [dict(r) for r in rows]


# 2.
class AlertsController:
    @classmethod
    async def get_alerts(cls, db: Session) -> List[AlertRowOut]:
        query = db.query(Alert).order_by(Alert.created_at.desc(), Alert.id.desc())
        return [AlertRowOut.model_validate(alert) for alert in query.all()]


@app.get("/alerts-second", response_model=List[AlertRowOut])
async def list_alerts_orm(db: Session = Depends(get_db)):
    return await AlertsController.get_alerts(db)
