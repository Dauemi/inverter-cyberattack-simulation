from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROFILE_CSV = PROJECT_ROOT / "data" / "france_sprint3" / "fr_load_profile_15min.csv"

def load_fr_load_profile():
    """
    Returns a DataFrame with:
      - timestamp
      - load_multiplier  (0–something, to scale peak loads)
    """
    df = pd.read_csv(PROFILE_CSV)
    # Make sure timestamps are real datetimes (optional but useful)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df