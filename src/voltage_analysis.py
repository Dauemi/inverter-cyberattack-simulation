import pandas as pd

BASE_CSV = "results/timeseries_BASE_no_attack_with_pv_profile.csv"
ATTACK_CSV = "results/timeseries_S3_attack_12_00_with_pv_profile.csv"

def main():
    base = pd.read_csv(BASE_CSV)
    atk = pd.read_csv(ATTACK_CSV)

    # Ensure timestamp is comparable
    base["timestamp"] = pd.to_datetime(base["timestamp"])
    atk["timestamp"] = pd.to_datetime(atk["timestamp"])

    # Merge on timestamp
    df = base[["timestamp", "min_vm_pu", "max_vm_pu"]].rename(
        columns={"min_vm_pu": "min_vm_base", "max_vm_pu": "max_vm_base"}
    ).merge(
        atk[["timestamp", "min_vm_pu", "max_vm_pu", "attack_applied"]],
        on="timestamp",
        how="inner",
        suffixes=("", "_atk")
    )

    df = df.rename(columns={"min_vm_pu": "min_vm_atk", "max_vm_pu": "max_vm_atk"})

    # Voltage drop (attack - base)
    df["delta_min_vm"] = df["min_vm_atk"] - df["min_vm_base"]

    # 1) Global stats
    print("=== VOLTAGE STABILITY SUMMARY (S3 vs BASE) ===")
    print(f"Overall min voltage (BASE):  {df['min_vm_base'].min():.4f} p.u.")
    print(f"Overall min voltage (ATTK):  {df['min_vm_atk'].min():.4f} p.u.")
    print(f"Worst voltage drop ΔV_min:   {df['delta_min_vm'].min():.4f} p.u.")

    # 2) Values at attack time
    attack_row = df[df["attack_applied"] == True].iloc[0]
    print("\n=== AT ATTACK TIME (12:00) ===")
    print(f"Min V base:   {attack_row['min_vm_base']:.4f} p.u.")
    print(f"Min V attack: {attack_row['min_vm_atk']:.4f} p.u.")
    print(f"ΔV_min:       {attack_row['delta_min_vm']:.4f} p.u.")

    # 3) Time steps where drop > 0.01 p.u. (example threshold)
    THRESH = -0.01  # -1% or worse
    critical = df[df["delta_min_vm"] <= THRESH]

    print(f"\nTime steps with ΔV_min <= {THRESH} p.u. (more than 1% drop):")
    if critical.empty:
        print("  None (attack impact is small in this network).")
    else:
        print(critical[["timestamp", "min_vm_base", "min_vm_atk", "delta_min_vm"]])

    # 4) Save detailed comparison CSV for your report
    out_path = "results/voltage_comparison_base_vs_S3.csv"
    df.to_csv(out_path, index=False)
    print(f"\nSaved detailed voltage comparison to: {out_path}")

if __name__ == "__main__":
    main()