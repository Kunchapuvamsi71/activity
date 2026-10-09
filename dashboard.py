"""Dashboard page and its JSON data endpoint."""
import os

from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.config import STATIC_DIR
from app.models import DailyActivity, get_db
from app.summary import build_summary

router = APIRouter()


@router.get("/", include_in_schema=False)
def index():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))


@router.get("/api/summary")
def summary(db: Session = Depends(get_db)):
    rows = [
        {
            "id": r.id,
            "subject_id": r.subject_id,
            "date": r.date.isoformat() if r.date else "",
            "steps": r.steps,
            "floors": r.floors,
            "intensity_mins_weekly_avg": r.intensity_mins_weekly_avg,
            "pal": r.pal,
            "active_mins": r.active_mins,
            "pai_score": r.pai_score,
        }
        for r in db.query(DailyActivity).all()
    ]
    return build_summary(rows)
