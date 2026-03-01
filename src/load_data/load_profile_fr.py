import pandas as pd

PROFILE_CSV = "data/france_sprint3/fr_load_profile_15min.csv"

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