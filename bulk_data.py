"""Generate ~7 months of random data for 6 subjects.  Run: python -m app.bulk_data"""
import datetime
import random

import requests

from app.config import API_URL

SUBJECTS = [f"n.{i}" for i in range(1, 7)]
ENTRIES_PER_SUBJECT = 30  # one entry per week, ~7 months


def main(seed=42):
    random.seed(seed)
    today = datetime.date.today()
    print("Generating 7 months of data for 6 subjects...")
    try:
        for subject in SUBJECTS:
            for i in range(ENTRIES_PER_SUBJECT):
                day = today - datetime.timedelta(weeks=ENTRIES_PER_SUBJECT - 1 - i)
                payload = {
                    "subject_id": subject,
                    "date": day.isoformat(),
                    "steps": random.randint(5000, 15000),
                    "floors": random.randint(2, 15),
                    "intensity_mins_weekly_avg": random.randint(150, 600),
                    "pal": round(random.uniform(1.2, 2.2), 2),
                    "active_mins": random.randint(30, 180),
                }
                requests.post(API_URL, json=payload, timeout=10).raise_for_status()
    except requests.RequestException as e:
        print(f"Request failed (is the server running?): {e}")
        return
    print("Done! Database populated.")


if __name__ == "__main__":
    main()
