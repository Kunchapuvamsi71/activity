"""API routes for receiving (simulated) Garmin watch data."""
import datetime
from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.calculator import PAICalculator
from app.models import DailyActivity, get_db

router = APIRouter()
calc = PAICalculator()


class ActivityPayload(BaseModel):
    subject_id: str = "unknown"
    date: Optional[datetime.date] = None  # defaults to today if omitted
    steps: int = Field(0, ge=0)
    floors: int = Field(0, ge=0)
    intensity_mins_weekly_avg: int = Field(0, ge=0)
    pal: float = Field(0.0, ge=0)
    active_mins: int = Field(0, ge=0)


@router.post("/garmin-webhook")
def receive_garmin_data(payload: ActivityPayload, db: Session = Depends(get_db)):
    data = {
        "steps": payload.steps,
        "floors": payload.floors,
        "intensity_mins_weekly_avg": payload.intensity_mins_weekly_avg,
        "pal": payload.pal,
        "active_mins": payload.active_mins,
    }
    score = calc.compute_daily_pai(data)

    entry = DailyActivity(
        subject_id=payload.subject_id,
        date=payload.date or datetime.date.today(),
        pai_score=score,
        **data,
    )
    db.add(entry)
    db.commit()
    return {"status": "success", "calculated_pai": score}
