from __future__ import annotations

from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

_ENGINE = None

def ENGINE():
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = create_engine("sqlite:///db.sqlite", connect_args={"check_same_thread": False})
    return _ENGINE




SessionLocal = sessionmaker(bind=ENGINE(), autoflush=False, autocommit=False)


def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
