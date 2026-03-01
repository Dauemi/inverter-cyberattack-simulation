import pandas as pd

ATTACK_CSV = "data/france_sprint3/fr_attack_scenarios_S1_S5.csv"

def load_attack_scenarios():
    """Return the full attack scenarios table as a DataFrame."""
    return pd.read_csv(ATTACK_CSV)

def get_scenario(scenario_name: str):
    """Return one row (as dict) for S1, S2, ..., S5."""
    df = load_attack_scenarios()
    row = df[df["scenario"] == scenario_name]
    if row.empty:
        raise ValueError(f"Scenario {scenario_name} not found")
    return row.iloc[0].to_dict()

def apply_attack_to_pv(net, scenario_name: str) -> float:
    """
    Sprint-3 logic:

    - Look up scenario S1–S5
    - Compute a global multiplier for the PV fleet.
    - We DO NOT modify net.sgen here; instead we return the multiplier.
      The time-series loop will apply it to the PV profile at each step.
    """
    info = get_scenario(scenario_name)

    compromised_pct = info["compromised_pct"]           # e.g. 5.0 (% of fleet)
    change_pct_of_affected = info["change_pct_of_affected"]  # usually -100
    ramp_seconds = info["ramp_seconds"]

    print(f"\n=== APPLYING ATTACK {scenario_name} ===")
    print(f"Description: {info['description']}")
    print(f"Compromised fleet: {compromised_pct}%")
    print(f"Change of affected PV: {change_pct_of_affected}%")
    print(f"Ramp (s): {ramp_seconds}")

    # Total PV before the attack (peak fleet capacity, not time-series shaped)
    total_pv_before = net.sgen["p_mw"].sum()
    print(f"Total PV fleet capacity (before attack): {total_pv_before:.3f} MW")

    frac_compromised = compromised_pct / 100.0
    change_frac = change_pct_of_affected / 100.0      # e.g. -1.0
    compromised_multiplier = 1.0 + change_frac        # e.g. 0.0

    # Fraction of fleet unaffected + affected scaled
    global_multiplier = (1 - frac_compromised) + frac_compromised * compromised_multiplier

    total_pv_after = total_pv_before * global_multiplier
    print(f"Effective fleet multiplier: {global_multiplier:.3f}")
    print(f"PV fleet capacity after attack (if fully sunny): {total_pv_after:.3f} MW")

    return global_multiplier