import math
import numpy as np
import pandas as pd
import pandapower as pp

from grid_topology.load_france_grid import load_france_grid
from load_data.load_profile_fr import load_fr_load_profile
from attacks.attack_fr import apply_attack_to_pv


def pv_shape_from_timestamp(ts: pd.Timestamp) -> float:
    """
    Same PV sunrise→sunset shape as in main.py.
    """
    hour = ts.hour + ts.minute / 60.0
    if hour <= 6 or hour >= 18:
        return 0.0
    x = (hour - 6) / 12.0 * math.pi  # 0 at 6:00, pi at 18:00
    val = math.sin(x)
    return max(0.0, min(1.0, val))


def compute_max_line_loading(with_attack: bool,
                             scenario: str = "S3",
                             attack_time_str: str = "2026-02-04 12:00:00") -> pd.DataFrame:
    """
    Run a 24h time-series and track, for each line:
      - maximum loading (%) over the day
      - loading (%) exactly at the attack time (12:00)
    If with_attack is False -> baseline case (no attack).
    If with_attack is True  -> apply S3 at 12:00.
    """
    net = load_france_grid()
    base_load = net.load["p_mw"].copy()
    base_pv = net.sgen["p_mw"].copy()

    profile = load_fr_load_profile()
    attack_time = pd.to_datetime(attack_time_str)

    # For each line, track maximum loading over all time steps
    max_loading = np.zeros(len(net.line))
    loading_at_attack = None

    fleet_multiplier = 1.0
    attack_applied = False

    for _, row in profile.iterrows():
        ts = row["timestamp"]
        mult = row["load_multiplier"]

        # Scale loads
        net.load["p_mw"] = base_load * mult

        # PV shape
        pv_shape = pv_shape_from_timestamp(ts)

        # Optional attack at 12:00
        if with_attack and (not attack_applied) and (ts == attack_time):
            print(f"Triggering attack {scenario} at {ts}")
            fleet_multiplier = apply_attack_to_pv(net, scenario)
            attack_applied = True

        # Apply PV profile + (maybe) attack derating
        net.sgen["p_mw"] = base_pv * pv_shape * fleet_multiplier

        # Power flow
        pp.runpp(net)

        loading = net.res_line["loading_percent"].values
        max_loading = np.maximum(max_loading, loading)

        if ts == attack_time:
            loading_at_attack = loading.copy()

    df = pd.DataFrame({
        "line_name": net.line["name"],
        "max_loading_percent": max_loading,
    })
    if loading_at_attack is not None:
        df["loading_at_attack_percent"] = loading_at_attack

    return df


def main():
    attack_time = "2026-02-04 12:00:00"
    scenario = "S3"

    # Baseline (no attack)
    print("\n=== Computing baseline line loading (no attack) ===")
    base_df = compute_max_line_loading(with_attack=False,
                                       scenario=scenario,
                                       attack_time_str=attack_time)
    base_df = base_df.rename(columns={
        "max_loading_percent": "max_loading_percent_base",
        "loading_at_attack_percent": "loading_at_attack_percent_base"
    })

    # Attack case
    print("\n=== Computing line loading with attack S3 ===")
    atk_df = compute_max_line_loading(with_attack=True,
                                      scenario=scenario,
                                      attack_time_str=attack_time)
    atk_df = atk_df.rename(columns={
        "max_loading_percent": "max_loading_percent_atk",
        "loading_at_attack_percent": "loading_at_attack_percent_atk"
    })

    # Merge on line name
    merged = base_df.merge(atk_df, on="line_name")

    # Difference in max loading over the day
    merged["delta_max_loading"] = (
        merged["max_loading_percent_atk"] - merged["max_loading_percent_base"]
    )

    # Summary
    print("\n=== LINE LOADING SUMMARY (S3 vs BASE) ===")
    print("Top 5 lines by max loading in attack case:")
    print(
        merged.sort_values("max_loading_percent_atk", ascending=False)
              .head(5)[
            ["line_name",
             "max_loading_percent_base",
             "max_loading_percent_atk",
             "delta_max_loading"]
        ]
    )

    # Overloaded lines (>100%)
    overloaded = merged[merged["max_loading_percent_atk"] > 100]
    if overloaded.empty:
        print("\nNo lines overloaded (>100%) in S3 scenario.")
    else:
        print("\nOverloaded lines in S3 scenario:")
        print(
            overloaded[
                ["line_name",
                 "max_loading_percent_base",
                 "max_loading_percent_atk",
                 "delta_max_loading"]
            ]
        )

    # High-stress lines (>80%) for "watch list"
    high = merged[merged["max_loading_percent_atk"] > 80]
    if high.empty:
        print("\nNo lines above 80% loading in S3 scenario.")
    else:
        print("\nLines above 80% loading in S3 scenario (watch list):")
        print(
            high[
                ["line_name",
                 "max_loading_percent_base",
                 "max_loading_percent_atk",
                 "delta_max_loading"]
            ]
        )

    # Save detailed comparison
    out_path = "results/line_loading_base_vs_S3.csv"
    merged.to_csv(out_path, index=False)
    print(f"\nSaved detailed line-loading comparison to: {out_path}")


if __name__ == "__main__":
    main()