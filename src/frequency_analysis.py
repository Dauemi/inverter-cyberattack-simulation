# IMPORTANT LIMITATION:
# This frequency deviation model is a simplified linear approximation used for
# high-level scenario comparison only.
#
# Formula used:
#   delta_f = -0.5 * (fraction_lost / 0.10)
#
# This assumes a direct proportional relationship between generation loss and
# system frequency deviation, without explicitly modelling:
# - system inertia,
# - swing equation dynamics,
# - primary frequency response (droop control),
# - spinning reserves / Frequency Containment Reserves (FCR),
# - governor response time.
#
# As a result, the model is not intended to represent the true dynamic frequency
# response of the European interconnected power system. It may overestimate
# frequency deviation for small disturbances and underestimate it for larger,
# time-dependent events.
#
# It is retained here as a transparent and reproducible first-order approximation
# for comparing cyberattack scenarios (S1-S5) within the project scope.~

from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ATTACK_CSV = PROJECT_ROOT / "data" / "france_sprint3" / "fr_attack_scenarios_S1_S5.csv"

# Assumed system properties (for the whole European / national grid)
P_SYS_GW = 100.0      # total online generation, in GW (assumption)
F_NOM = 50.0          # nominal frequency, Hz
SENS_10pct = 0.5      # frequency drop (Hz) if 10% of generation is lost


def estimate_delta_f(fraction_lost: float) -> float:
    """
    Simple frequency sensitivity model:
    - If 10% of total generation is lost -> 0.5 Hz drop
    - Scale linearly with fraction_lost
    Δf = -SENS_10pct * (fraction_lost / 0.10)
    NOTE: This is a toy model that ignores inertia, primary control (FCR),
    and system dynamics. It is used for illustrative impact ranking only.
    """
    return -SENS_10pct * (fraction_lost / 0.10)


def main():
    df = pd.read_csv(ATTACK_CSV)

    results = []

    for _, row in df.iterrows():
        scenario = row["scenario"]
        desc = row["description"]
        affected_power_gw = row["affected_power_gw"]
        change_pct_of_affected = row["change_pct_of_affected"]  # typically -100

        # Effective lost power (GW)
        lost_frac_of_affected = abs(change_pct_of_affected) / 100.0
        delta_p_gw = affected_power_gw * lost_frac_of_affected

        # Fraction of total system generation that is lost
        fraction_lost = delta_p_gw / P_SYS_GW  # unitless

        # Estimated frequency deviation
        delta_f_hz = estimate_delta_f(fraction_lost)

        # Simple qualitative classification
        severity = "Low"
        if abs(delta_f_hz) >= 0.1:
            severity = "Moderate"
        if abs(delta_f_hz) >= 0.3:
            severity = "High"
        if abs(delta_f_hz) >= 0.8:
            severity = "Critical"

        results.append({
            "scenario": scenario,
            "description": desc,
            "affected_power_gw": affected_power_gw,
            "delta_p_gw": delta_p_gw,
            "fraction_lost": fraction_lost,
            "delta_f_hz": delta_f_hz,
            "severity": severity,
        })

    out_df = pd.DataFrame(results)

    print("=== FREQUENCY IMPACT ESTIMATION (Toy Model) ===")
    print(f"Assumed system size P_sys = {P_SYS_GW} GW, f_nom = {F_NOM} Hz")
    print(f"Assumed: 10% loss of generation -> {SENS_10pct} Hz drop\n")

    print(out_df[[
        "scenario",
        "affected_power_gw",
        "delta_p_gw",
        "fraction_lost",
        "delta_f_hz",
        "severity"
    ]])

    # Save for your report
    out_path = "results/frequency_impact_S1_S5.csv"
    out_df.to_csv(out_path, index=False)
    print(f"\nSaved frequency impact table to: {out_path}")


if __name__ == "__main__":
    main()