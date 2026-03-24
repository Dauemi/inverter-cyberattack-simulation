# Things to KNOW
Folder 1. dashboard/ → Visualization Layer
Files:

combined_dashboard.json

build_dashboard_data.py

README.md

Purpose: This is where results are prepared for visualization.

What it does:

Takes processed data (risk scores, scenarios)

Formats it into dashboard-ready structure (likely JSON)

Used for reporting / presentation

👉 In simple terms: “This folder turns raw simulation outputs into something we can display visually (charts, dashboards, reports).”


# 2ASICYA Dashboard

## Open the dashboard

- Open `2ASICYA_Dashboard.html` in any browser (Chrome, Firefox, Edge).
- No installation required (Plotly.js is loaded via CDN).
- Internet is needed on the first load (for Plotly.js).

## Tabs

- **Overview**: KPIs, PV production, load profile, bus voltages, line loading.
- **Attack Simulation**: S1–S5 scenario selector, generation comparison, frequency impact, voltage impact.
- **IDS & Security**: alerts, detection rate, MITRE ATT&CK ICS types, alert feed.
- **Grid & Topology**: 33-bus visualization, inverter and PV tables, PV stack, load distribution.
- **Risk Matrix**: likelihood vs impact, risk scores per scenario.

## Recommended Kaggle datasets

- Solar Power Generation Data (22 inverters, 15‑min):  
  https://www.kaggle.com/datasets/anikannal/solar-power-generation-data
- Smart Grid Intrusion Detection:  
  https://www.kaggle.com/datasets/hussainsheikh03/smart-grid-intrusion-detection-dataset

## Notes

- The dashboard data is embedded in the HTML under `const D = {...}`.
- Replace that JSON manually or regenerate it with a Python script.

## Combined data build (France + Kaggle)

1) Put the Kaggle CSVs in `dashboard/data/` (generation + weather files).
2) Make sure France Sprint 3 CSVs are in `data/france_sprint3/`.
3) Run:

```bash
python dashboard/build_dashboard_data.py \
  --html ../2ASICYA_Dashboard.html \
  --out dashboard/data/combined_dashboard.json \
  --france-dir data/france_sprint3 \
  --kaggle-dir dashboard/data \
  --inject
```

This will update the HTML (`const D = {...}`) and keep the dashboard static but refreshed.
