"""Physical Activity Index (PAI) calculation."""


class PAICalculator:
    def __init__(self):
        # Reference thresholds from the research paper, Table I
        self.thresholds = {
            "steps": 10000,
            "floors": 8,
            "intensity_minutes_week": 450,
            "pal": 1.85,
            "active_minutes": 120,
        }
        self.weight = 1 / len(self.thresholds)  # wi = 1/N (N = 5 parameters)

    @staticmethod
    def calculate_partial_percentage(value, threshold):
        """pi: partial percentage of activity, capped at 1.0."""
        if value is None or value <= 0:
            return 0.0
        if value >= threshold:
            return 1.0
        return value / threshold

    def compute_daily_pai(self, daily_data):
        """daily_data: dict containing activity metrics. Returns PAI in 0-100."""
        t = self.thresholds
        partials = [
            self.calculate_partial_percentage(daily_data.get("steps", 0), t["steps"]),
            self.calculate_partial_percentage(daily_data.get("floors", 0), t["floors"]),
            self.calculate_partial_percentage(
                daily_data.get("intensity_mins_weekly_avg", 0), t["intensity_minutes_week"]
            ),
            self.calculate_partial_percentage(daily_data.get("pal", 0), t["pal"]),
            self.calculate_partial_percentage(daily_data.get("active_mins", 0), t["active_minutes"]),
        ]
        # Formula from paper: PAI = sum(wi * pi)
        return round(self.weight * sum(partials) * 100, 2)
