# src/metrics.py

def compute_voltage_metrics(df, v_min, v_max):
    undervoltage = (df["voltage"] < v_min).sum()
    overvoltage = (df["voltage"] > v_max).sum()

    total = len(df)

    return {
        "undervoltage_pct": 100 * undervoltage / total,
        "overvoltage_pct": 100 * overvoltage / total,
    }