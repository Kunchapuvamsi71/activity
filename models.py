"""Database models and session handling."""
import os

from sqlalchemy import Column, Date, Float, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import DB_PATH

Base = declarative_base()


class DailyActivity(Base):
    __tablename__ = "daily_activities"

    id = Column(Integer, primary_key=True)
    subject_id = Column(String(50), index=True)
    date = Column(Date)
    steps = Column(Integer)
    floors = Column(Integer)
    intensity_mins_weekly_avg = Column(Integer)
    pal = Column(Float)
    active_mins = Column(Integer)
    pai_score = Column(Float)


os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    """FastAPI dependency: yields a session and always closes it."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
