"""Shared paths and constants (no third-party imports)."""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.environ.get("PAI_DB_PATH", os.path.join(DB_DIR, "physical_activity.db"))
STATIC_DIR = os.path.join(BASE_DIR, "static")
RESULTS_DIR = os.path.join(os.path.dirname(BASE_DIR), "results")

API_URL = os.environ.get("PAI_API_URL", "http://127.0.0.1:8000/garmin-webhook")
