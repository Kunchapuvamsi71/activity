from app.summary import build_summary


def row(i, sid, date, steps, active, pai):
    return {"id": i, "subject_id": sid, "date": date, "steps": steps,
            "active_mins": active, "pai_score": pai}


def test_empty():
    s = build_summary([])
    assert s["total"] == 0 and s["subjects"] == [] and s["overall_avg_pai"] is None
    assert s["correlation_steps_active"] is None


def test_per_subject_average_and_order():
    rows = [row(1, "n.2", "2026-01-02", 1, 1, 80), row(2, "n.1", "2026-01-01", 2, 2, 60),
            row(3, "n.1", "2026-01-03", 3, 3, 100)]
    s = build_summary(rows)
    assert [x["subject_id"] for x in s["subjects"]] == ["n.1", "n.2"]
    assert s["subjects"][0]["avg_pai"] == 80.0 and s["subjects"][0]["count"] == 2
    assert [p["date"] for p in s["series"]["n.1"]] == ["2026-01-01", "2026-01-03"]


def test_correlation_and_recent_limit():
    rows = [row(i, "n.1", f"2026-01-{i:02d}", i * 100, i * 10, 50) for i in range(1, 16)]
    s = build_summary(rows, recent_n=5)
    assert s["correlation_steps_active"] == 1.0
    assert len(s["recent"]) == 5 and s["recent"][0]["id"] == 15


def test_constant_input_correlation_is_none():
    rows = [row(1, "n.1", "2026-01-01", 5, 5, 50), row(2, "n.1", "2026-01-02", 5, 5, 50)]
    assert build_summary(rows)["correlation_steps_active"] is None
