import os
import pandas as pd

# NOTE:
# Default impact/likelihood scores are expert-assigned for the report.
# If you have computed scores, place them in results/risk_scores_S1_S5.csv
# with columns: scenario,impact,likelihood. They will override defaults.

# Define impact and likelihood scores for S1-S5
data = [
    ("S1", 1, 3),
    ("S2", 2, 3),
    ("S3", 2, 4),
    ("S4", 3, 4),
    ("S5", 4, 2)
]

SCORES_CSV = "results/risk_scores_S1_S5.csv"
if os.path.exists(SCORES_CSV):
    df = pd.read_csv(SCORES_CSV)
else:
    df = pd.DataFrame(data, columns=["scenario", "impact", "likelihood"])
df["risk_score"] = df["impact"] * df["likelihood"]

def classify(score):
    if score <= 3:
        return "Low"
    elif score <= 6:
        return "Low–Medium"
    elif score <= 9:
        return "Medium"
    elif score <= 12:
        return "High"
    else:
        return "Critical"

df["risk_level"] = df["risk_score"].apply(classify)

print(df)

# Save for your report
df.to_csv("results/risk_matrix_S1_S5.csv", index=False)
print("\nSaved risk matrix to results/risk_matrix_S1_S5.csv")