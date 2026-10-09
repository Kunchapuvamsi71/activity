import pytest

from app.calculator import PAICalculator

calc = PAICalculator()


def test_all_thresholds_met_gives_100():
    data = {"steps": 10000, "floors": 8, "intensity_mins_weekly_avg": 450,
            "pal": 1.85, "active_mins": 120}
    assert calc.compute_daily_pai(data) == 100.0


def test_values_above_threshold_are_capped():
    data = {"steps": 50000, "floors": 100, "intensity_mins_weekly_avg": 5000,
            "pal": 5, "active_mins": 1000}
    assert calc.compute_daily_pai(data) == 100.0


def test_empty_input_gives_zero():
    assert calc.compute_daily_pai({}) == 0.0


def test_paper_example_subject():
    data = {"steps": 12500, "floors": 12, "intensity_mins_weekly_avg": 400,
            "pal": 1.9, "active_mins": 135}
    assert calc.compute_daily_pai(data) == pytest.approx(97.78, abs=0.01)


def test_partial_percentage_none_and_negative():
    assert calc.calculate_partial_percentage(None, 10) == 0.0
    assert calc.calculate_partial_percentage(-5, 10) == 0.0
