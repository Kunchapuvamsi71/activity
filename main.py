"""Application entry point.  Run from the project root:

    uvicorn app.main:app --reload

Dashboard: http://127.0.0.1:8000/   API docs: http://127.0.0.1:8000/docs
"""
from fastapi import FastAPI

from app.api_handler import router
from app.dashboard import router as dashboard_router
from app.models import init_db

app = FastAPI(title="Garmin PAI IoT Platform")


@app.on_event("startup")
def on_startup():
    init_db()


app.include_router(router)
app.include_router(dashboard_router)
