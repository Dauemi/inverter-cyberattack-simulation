import math
import os
import sys
from pathlib import Path

import pandas as pd
import pandapower as pp

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.grid_topology.load_france_grid import load_france_grid
from src.load_data.load_profile_fr import load_fr_load_profile
from src.attacks.attack_fr import apply_attack_to_pv


ATTACK_CSV = "data/france_sprint3/fr_attack_scenarios_S1_S5.csv"
OUT_CSV = "results/risk_scores_S1_S5.csv"

P_SYS_GW = 100.0
SENS_10pct = 0.5  # Hz drop for 10% loss


def pv_shape_from_timestamp(ts: pd.Timestamp) -> float:
    hour = ts.hour + ts.minute / 60.0
    if hour <= 6 or hour >= 18:
        return 0.0
    x = (hour - 6) / 12.0 * math.pi
    return max(0.0, min(1.0, math.sin(x)))


def compute_metrics_for_scenario(scenario: str) -> dict:
    net = load_france_grid()
    base_load = net.load["p_mw"].copy()
    base_pv = net.sgen["p_mw"].copy()
    profile = load_fr_load_profile()
    attack_time = pd.to_datetime("2026-02-04 12:00:00")

    max_line_loading = 0.0
    min_vm = 10.0
    max_vm = 0.0
    fleet_multiplier = 1.0
    attack_applied = False

    for _, row in profile.iterrows():
        ts = row["timestamp"]
        mult = row["load_multiplier"]
        net.load["p_mw"] = base_load * mult

        if (not attack_applied) and (ts == attack_time):
            fleet_multiplier = apply_attack_to_pv(net, scenario)
            attack_applied = True

        pv_shape = pv_shape_from_timestamp(ts)
        net.sgen["p_mw"] = base_pv * pv_shape * fleet_multiplier
        pp.runpp(net)

        max_line_loading = max(max_line_loading, net.res_line["loading_percent"].max())
        min_vm = min(min_vm, net.res_bus["vm_pu"].min())
        max_vm = max(max_vm, net.res_bus["vm_pu"].max())

    return {
        "max_line_loading": max_line_loading,
        "min_vm": min_vm,
        "max_vm": max_vm,
    }


def impact_from_metrics(metrics: dict, delta_f_hz: float) -> int:
    # Voltage deviation magnitude
    dv = max(abs(metrics["min_vm"] - 1.0), abs(metrics["max_vm"] - 1.0))
    # Line loading
    ll = metrics["max_line_loading"]
    # Frequency deviation
    df = abs(delta_f_hz)

    score = 0
    if dv >= 0.02:
        score += 1
    if dv >= 0.05:
        score += 1
    if ll >= 80:
        score += 1
    if ll >= 100:
        score += 1
    if df >= 0.1:
        score += 1
    if df >= 0.3:
        score += 1

    # Map to 1..5
    if score <= 1:
        return 1
    if score == 2:
        return 2
    if score == 3:
        return 3
    if score == 4:
        return 4
    return 5


def estimate_delta_f(affected_power_gw: float, change_pct_of_affected: float) -> float:
    delta_p_gw = affected_power_gw * (abs(change_pct_of_affected) / 100.0)
    fraction_lost = delta_p_gw / P_SYS_GW
    return -SENS_10pct * (fraction_lost / 0.10)


def main():
    df = pd.read_csv(ATTACK_CSV)

    # Likelihood: inverse of affected power rank (bigger attack -> less likely)
    df = df.sort_values("affected_power_gw", ascending=False).reset_index(drop=True)
    df["likelihood"] = df.index.map(lambda i: max(1, 5 - i))

    impacts = []
    for _, row in df.iterrows():
        scenario = row["scenario"]
        delta_f = estimate_delta_f(row["affected_power_gw"], row["change_pct_of_affected"])
        metrics = compute_metrics_for_scenario(scenario)
        impact = impact_from_metrics(metrics, delta_f)
        impacts.append(impact)

    df["impact"] = impacts
    df["risk_score"] = df["impact"] * df["likelihood"]

    out = df[["scenario", "impact", "likelihood", "risk_score"]].sort_values("scenario")
    os.makedirs("results", exist_ok=True)
    out.to_csv(OUT_CSV, index=False)
    print(f"Saved risk scores to {OUT_CSV}")


if __name__ == "__main__":
    main()
