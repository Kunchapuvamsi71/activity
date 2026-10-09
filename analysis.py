"""Analyse stored data.  Run from project root: python -m app.analysis [--show]"""
import os
import sqlite3
import sys

import matplotlib

if "--show" not in sys.argv:
    matplotlib.use("Agg")  # headless-safe
import matplotlib.pyplot as plt
import pandas as pd

from app.config import DB_PATH, RESULTS_DIR


def run_analysis(show=False):
    if not os.path.exists(DB_PATH):
        print(f"No database at {DB_PATH}. Start the server and run bulk_data first.")
        return

    with sqlite3.connect(DB_PATH) as conn:
        try:
            df = pd.read_sql_query("SELECT * FROM daily_activities", conn)
        except pd.errors.DatabaseError:
            print("Table 'daily_activities' not found. Start the server once to create it.")
            return

    if df.empty:
        print("Database is empty!")
        return

    # 1. Average PAI per subject
    avg_pai = df.groupby("subject_id")["pai_score"].mean()
    print("--- Results ---")
    print(avg_pai.round(2))

    # 2. Correlation (Table II)
    correlation = df["steps"].corr(df["active_mins"])
    print(f"\nCorrelation (Steps vs Active Mins): {correlation:.4f}")

    # 3. Plot (Fig 3)
    plt.figure(figsize=(10, 6))
    avg_pai.plot(kind="bar", color="skyblue")
    plt.title("Physical Activity Index (PAI) per Subject")
    plt.xlabel("Subject ID")
    plt.ylabel("Average PAI %")
    plt.xticks(rotation=0)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()

    os.makedirs(RESULTS_DIR, exist_ok=True)
    out = os.path.join(RESULTS_DIR, "pai_per_subject.png")
    plt.savefig(out, dpi=150)
    print(f"\nChart saved to {out}")
    if show:
        plt.show()


if __name__ == "__main__":
    run_analysis(show="--show" in sys.argv)
