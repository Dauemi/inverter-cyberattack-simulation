import sys
import pandas as pd
import pandapower as pp

from src.grid_topology.load_france_grid import load_france_grid
from src.load_data.load_profile_fr import load_fr_load_profile
from src.attacks.attack_fr import apply_attack_to_pv


def pv_shape_from_timestamp(ts: pd.Timestamp) -> float:
    hour = ts.hour + ts.minute / 60.0
    if hour <= 6 or hour >= 18:
        return 0.0
    return max(0.0, min(1.0, __import__("math").sin((hour - 6) / 12.0 * __import__("math").pi)))


def main():
    scenarios = ["S1", "S2", "S3", "S4", "S5"]
    net = load_france_grid()
    base_load = net.load["p_mw"].copy()
    base_pv = net.sgen["p_mw"].copy()

    profile = load_fr_load_profile()
    attack_time = pd.to_datetime("2026-02-04 12:00:00")
    row = profile[profile["timestamp"] == attack_time]
    if row.empty:
        print("ERROR: attack timestamp not found in load profile.")
        sys.exit(1)
    mult = row.iloc[0]["load_multiplier"]

    for sc in scenarios:
        net.load["p_mw"] = base_load * mult
        pv_shape = pv_shape_from_timestamp(attack_time)
        fleet_multiplier = apply_attack_to_pv(net, sc)
        net.sgen["p_mw"] = base_pv * pv_shape * fleet_multiplier
        pp.runpp(net)
        print(f"{sc}: OK (max line loading = {net.res_line['loading_percent'].max():.2f}%)")

    print("Smoke test passed for S1–S5.")


if __name__ == "__main__":
    main()
