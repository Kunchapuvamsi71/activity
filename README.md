# Garmin PAI IoT Platform

A small simulated IoT pipeline that receives Garmin-style smartwatch data, computes a
**Physical Activity Index (PAI)** per day, stores it in SQLite, and analyses results per subject.
It replicates the PAI method (Table I thresholds, Table II correlation, Fig. 3 chart) from a research paper.

## How PAI is computed

Each day is scored on five metrics against a reference threshold. Each partial score is capped at 100%
and the PAI is their equal-weighted average (wi = 1/5):

| Metric | Threshold |
|---|---|
| Steps | 10,000 |
| Floors climbed | 8 |
| Intensity minutes (weekly avg) | 450 |
| Physical activity level (PAL) | 1.85 |
| Active minutes | 120 |

## Project structure

```
app/
  config.py         paths / URL settings
  models.py         SQLAlchemy model + DB session
  calculator.py     PAI calculation
  api_handler.py    POST /garmin-webhook route
  main.py           FastAPI app entry point
  dashboard.py      serves the dashboard page + GET /api/summary
  summary.py        summary statistics used by the dashboard
  static/index.html web dashboard (no external dependencies)
  simulate_watch.py send one sample reading
  bulk_data.py      generate ~7 months of data for 6 subjects
  analysis.py       averages, correlation, chart
tests/              unit tests
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Usage (run everything from the project root)

```bash
# 1. Start the server
uvicorn app.main:app --reload

# 2. In another terminal: send data
python -m app.simulate_watch     # one reading
python -m app.bulk_data          # 180 random readings

# 3. Analyse
python -m app.analysis           # saves results/pai_per_subject.png (add --show to open it)
```

- **Dashboard:** http://127.0.0.1:8000/ shows stats, an average-PAI bar chart, PAI over time, recent readings, and a form to send a reading.
- **API docs:** http://127.0.0.1:8000/docs

### Example request

```bash
curl -X POST http://127.0.0.1:8000/garmin-webhook \
  -H "Content-Type: application/json" \
  -d '{"subject_id":"n.1","steps":12500,"floors":12,"intensity_mins_weekly_avg":400,"pal":1.9,"active_mins":135}'
# {"status":"success","calculated_pai":97.78}
```

`date` (YYYY-MM-DD) is optional and defaults to today.

## Tests

```bash
pip install -r requirements-dev.txt
pytest
```

## Note

All data is randomly generated for simulation; results do not represent real subjects.

## License

MIT
