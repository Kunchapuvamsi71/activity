"""Send one simulated watch reading for subject n.1.  Run: python -m app.simulate_watch"""
import requests

from app.config import API_URL

# Metrics based on Table I of the paper
data = {
    "subject_id": "n.1",
    "steps": 12500,                    # target 10,000
    "floors": 12,                      # target 8
    "intensity_mins_weekly_avg": 400,  # target 450
    "pal": 1.9,                        # target 1.85
    "active_mins": 135,                # target 120
}


def main():
    print(f"Sending data to IoT platform: {data}")
    try:
        response = requests.post(API_URL, json=data, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return
    result = response.json()
    print("\n--- Experiment Results ---")
    print(f"Status: {result['status']}")
    print(f"Calculated Daily PAI Score: {result['calculated_pai']}%")


if __name__ == "__main__":
    main()
