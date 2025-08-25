import pandas as pd

def summarize_metrics(csv_path="data/metrics.csv", feature=""):
    df = pd.read_csv(csv_path, parse_dates=["date"])
    mask = df["feature"].str.contains(feature, case=False, na=False) if feature else df["feature"].notna()
    recent = df[mask].sort_values("date").tail(30)
    if recent.empty:
        return {"feature": feature, "note": "no recent data"}
    return {
        "feature": feature or "all",
        "avg_active_users": float(round(recent["active_users"].mean(), 1)),
        "avg_errors": float(round(recent["errors"].mean(), 2)),
        "avg_csat": float(round(recent["csat"].mean(), 2)),
    }
