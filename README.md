
---

## 🎯 Project Objective

![ECE Paris](https://img.shields.io/badge/ECE%20Paris-Cyber%20Physical%20Systems-003366)
![Smart Grid](https://img.shields.io/badge/Domain-Smart%20Grid%20Security-red)
![pandapower](https://img.shields.io/badge/Simulation-pandapower-success)
![Analysis](https://img.shields.io/badge/Analysis-Time%20Series-blueviolet)

Model, simulate, and evaluate the impact of coordinated cyberattacks on distributed solar PV inverters in the French electricity network by:

1. Creating a realistic distribution grid using **pandapower** and FR synthetic datasets.  
2. Simulating solar inverter shutdown attacks in scenarios S1–S5.  
3. Running **time-series load & PV curves** (15-minute resolution).  
4. Evaluating the impact on:
   - Bus voltages  
   - Line loadings  
   - System frequency  
5. Quantifying cyber-physical risk (impact × likelihood).  
6. Designing a 3-layer IDS architecture for detecting coordinated PV manipulation attacks.

---

# 🗂️ Dataset Overview (France Synthetic Sprint 3)

The simulation uses realistic **synthetic** (NOT confidential) French distribution data:

| Dataset | Description |
|--------|-------------|
| `fr_grid_buses.csv` | 33-bus distribution topology |
| `fr_grid_lines.csv` | 37 lines with impedances |
| `fr_grid_loads.csv` | 32 loads |
| `fr_grid_pv_generators.csv` | 7 aggregated PV generators |
| `fr_inverter_parameters.csv` | PV inverter characteristics |
| `fr_load_profile_15min.csv` | 15-min French load curve |
| `fr_attack_scenarios_S1_S5.csv` | Defined cyberattack levels |

This dataset is fully **public and research-safe**.

---

# 📡 Cyberattack Scenarios (S1–S5)

| Scenario | Description | PV Affected |
|----------|-------------|-------------|
| **S1** | Local disturbance | 0.1 GW |
| **S2** | Feeder-level coordinated attack | 0.4 GW |
| **S3** | Multi-region attack | 1.0 GW |
| **S4** | Regional synchronized shutdown | 2.0 GW |
| **S5** | National-scale coordinated shutdown | 5.0 GW |

PV is shut down **100%** in affected regions, triggered at **12:00**.

---

# ⚡ Simulation Workflow

## ✔ 1. Grid Initialization (pandapower)
Loads:
- Bus data
- Lines (R, X)
- Loads (MW)
- PV generators (MW)
- Slack grid

## ✔ 2. Load & PV Time-Series
- 15-minute load profile  
- Synthetic PV profile: sunrise → sunset  
- Combined into time-series power-flow loop

## ✔ 3. Attack Injection
At t = 12:00:
- Affected PV capacity is reduced based on S1–S5
- Scenarios automatically modify total PV output

## ✔ 4. Power-Flow Evaluation
For each timestep:
- `pp.runpp()`
- Record:
  - min/max voltage
  - line loading
  - total load, total PV

---

# 📊 Key Results (Dashboard‑Driven)

## 🔹 Voltage Stability
The exact values depend on the **combined dashboard dataset** (France Sprint3 + Kaggle).
Open the dashboard and use **RUN + RELOAD** to view updated voltage statistics.

---

## 🔹 Line Loading
Line loading metrics are computed from the current dataset.  
Refer to the **dashboard charts** for the latest max loading and overload indicators.

---

## 🔹 Frequency Impact (Simplified Model)
Frequency impact is **derived from a simplified sensitivity model**.  
Exact values are shown in the dashboard after data refresh.

**Current run (synthetic dataset):**

| Scenario | ΔP (GW) | Δf (Hz) | Severity |
|---------|----------|---------|----------|
| S1 | 0.1 | –0.005 | Low |
| S2 | 0.4 | –0.020 | Low |
| S3 | 1.0 | –0.050 | Low |
| S4 | 2.0 | –0.100 | Low |
| S5 | 5.0 | –0.250 | Moderate |

---

# 📉 Risk Matrix (Impact × Likelihood)
Risk scores are **computed from voltage, frequency, and line‑loading metrics**  
and displayed in the **dashboard Risk Matrix tab**.  
The exact table updates after running:
```
python scripts/compute_risk_scores.py
python dashboard/build_dashboard_data.py --html 2ASICYA_Dashboard.html --out dashboard/data/combined_dashboard.json --france-dir data/france_sprint3 --kaggle-dir dashboard/data --inject
```

**Current run (synthetic dataset):**

| Scenario | Impact | Likelihood | Risk Score | Risk Level |
|----------|--------|------------|------------|------------|
| S1 | 1 | 1 | 1 | Low |
| S2 | 1 | 2 | 2 | Low |
| S3 | 1 | 3 | 3 | Low |
| S4 | 1 | 4 | 4 | Low–Medium |
| S5 | 1 | 5 | 5 | Low–Medium |

---

# 🔐 IDS Architecture (Three-Layer Model)

## 🟦 1. Local Inverter IDS
Monitors:
- Sudden PV drop  
- Frequent setpoint changes  
- Invalid SunSpec/Modbus commands  
- Heartbeat loss  

Triggers:
- ΔP > 10% in 1 min  
- >10 identical commands in 5 sec  

---

## 🟧 2. Feeder/Substation IDS  
Detects:
- Coordinated feeder-wide shutdown  
- Voltage sag across multiple buses  
- Identical communication patterns from many inverters  

Triggers:
- Feeder PV loss > 30% in 5 min  
- >3 buses drop > 0.02 p.u.  

---

## 🟥 3. Control Center IDS (Wide-Area)
Detects:
- Multi-region S3/S4 attacks  
- National-level S5 shutdown  
- SCADA anomalies  
- Δf > 0.1 Hz  

Triggers:
- ΔP > 1 GW → High  
- ΔP > 5 GW → Critical  

---

# 🛠️ How to Run the Simulation

Install dependencies:

```bash
pip install -r requirements.txt
python -m src.main
```

## ✅ Test Checklist (Quick)

1) Install dependencies:
```bash
pip install -r requirements.txt
```

2) Ensure all France Sprint 3 CSVs exist in `data/france_sprint3/`:
- `fr_grid_buses.csv`
- `fr_grid_lines.csv`
- `fr_grid_loads.csv`
- `fr_grid_pv_generators.csv`
- `fr_inverter_parameters.csv`
- `fr_load_profile_15min.csv`
- `fr_attack_scenarios_S1_S5.csv`

3) Run the main simulation:
```bash
python -m src.main
```

If any CSV is missing, the simulation will fail.

4) Smoke test S1–S5 scenarios:
```bash
python scripts/smoke_scenarios.py
```

---

# ⚠️ Limitations (Summary)

- Simplified linear frequency model (no inertia or FCR).
- Local-scale feeder (33-bus, 3 MW PV) extrapolated to GW scenarios.
- IDS is conceptual (no real-time implementation).

---

# 🧭 Methodology (Summary)

- Pandapower: power-flow and time-series profiles (33-bus synthetic France).
- Frequency model: aggregated impact estimate (assumption P_sys=100 GW).

## Models used

- `src/full_simulation.py`: pandapower time-series + Monte Carlo summary.
- `src/resilience_auto_solver.py`: simplified ODE resilience experiment (mitigation vs no-mitigation).

---

# 📥 Kaggle Datasets (Dashboard)

- Solar Power Generation Data: https://www.kaggle.com/datasets/anikannal/solar-power-generation-data
- Smart Grid Intrusion Detection: https://www.kaggle.com/datasets/hussainsheikh03/smart-grid-intrusion-detection-dataset

---

# 🗂️ Project Structure

- `src/`: simulation, analysis, risk, and plotting modules.
- `data/france_sprint3/`: synthetic France datasets (CSV + metadata).
- `dashboard/`: dashboard guide and data placeholders.
- `backend/`: real-time FastAPI + WebSocket backend (Render).
- `realtime/`: Three.js 3D real-time viewer.

---

# 🧪 Real-Time 3D (Render + Vercel)

## Backend (Render)
1) Deploy using `render.yaml` (FastAPI + WebSocket).
2) After deployment, copy the WebSocket URL:
   `wss://YOUR-RENDER-APP.onrender.com/ws`

## Frontend (Vercel)
1) Open `realtime/index.html`.
2) Paste the WebSocket URL into the input.
3) Click **Connect** and choose scenario.

---

# 👥 Team Contributions

- Roy: simulation code, attack scenarios, results.
- Gilles: dashboard, data integration, visualizations.
- Eseoghene: document coordination and synthesis.
- Rasaq: security/IDS, risk matrix.
- Yves: external datasets, dashboard enrichment.
- Gémima: proofreading, consistency, finalization.
