"""Pure-Python summary statistics for the dashboard (no third-party imports)."""
import statistics
from collections import defaultdict


def _pearson(xs, ys):
    try:
        return round(statistics.correlation(xs, ys), 4)
    except (statistics.StatisticsError, ValueError):
        return None  # fewer than 2 points or constant input


def build_summary(rows, recent_n=10):
    """rows: list of dicts with subject_id, date (ISO str), steps, active_mins, pai_score, ..."""
    by_subject = defaultdict(list)
    for r in rows:
        by_subject[r["subject_id"]].append(r)

    subjects = []
    series = {}
    for sid in sorted(by_subject):
        items = sorted(by_subject[sid], key=lambda r: r["date"])
        scores = [r["pai_score"] for r in items]
        subjects.append({
            "subject_id": sid,
            "count": len(items),
            "avg_pai": round(sum(scores) / len(scores), 2),
        })
        series[sid] = [{"date": r["date"], "pai": r["pai_score"]} for r in items]

    recent = sorted(rows, key=lambda r: (r["date"], r.get("id", 0)), reverse=True)[:recent_n]
    return {
        "total": len(rows),
        "overall_avg_pai": round(sum(r["pai_score"] for r in rows) / len(rows), 2) if rows else None,
        "correlation_steps_active": _pearson([r["steps"] for r in rows],
                                             [r["active_mins"] for r in rows]),
        "subjects": subjects,
        "series": series,
        "recent": recent,
    }
