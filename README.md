# 2ASICYA — Solar Inverter Cyber Attack Simulation

This repository contains the full MSc project implementation for cyber-physical attack simulation on distributed PV inverters, including:
- offline simulation and risk analysis,
- an interactive analytics dashboard,
- and a real-time 3D digital-twin style cyberattack viewer.

---

## 🎯 Project Objective

![ECE Paris](https://img.shields.io/badge/ECE%20Paris-Cyber%20Physical%20Systems-003366)
![Smart Grid](https://img.shields.io/badge/Domain-Smart%20Grid%20Security-red)
![pandapower](https://img.shields.io/badge/Simulation-pandapower-success)
![Analysis](https://img.shields.io/badge/Analysis-Time%20Series-blueviolet)
![Testing](https://img.shields.io/badge/Testing-pytest-green)

Model, simulate, and evaluate the impact of coordinated cyberattacks on distributed solar PV inverters in the French electricity network by:

1. Creating a realistic distribution grid using **pandapower** and FR synthetic datasets  
2. Simulating solar inverter shutdown attacks in scenarios S1–S5  
3. Running **time-series load & PV curves** (15-minute resolution)  
4. Evaluating the impact on:
   - Bus voltages  
   - Line loadings  
   - System frequency  
5. Quantifying cyber-physical risk (impact × likelihood)  
6. Designing a 3-layer IDS architecture for detecting coordinated PV manipulation attacks
7. Project aims to fill the gap between renewable deployment and cybersecurity maturity  

---

# 🗂️ Dataset Overview (France Synthetic Sprint 3)

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
- Synthetic PV profile (sunrise → sunset)  
- Combined into time-series simulation  

## ✔ 3. Attack Injection
At t = 12:00:
- PV generation is reduced based on scenario magnitude  
- Scenarios dynamically modify total PV output  

## ✔ 4. Power-Flow Evaluation
For each timestep:
- `pp.runpp()`  
- Record:
  - Min/max voltage  
  - Line loading  
  - Total load and PV  

---

# 📊 Key Results (Dashboard-Driven)

## 🔹 Voltage Stability
Values depend on the **combined dataset (France Sprint3 + Kaggle)**.  
Use the dashboard (**RUN + RELOAD**) for updated results.

## 🔹 Line Loading
Line loading metrics are computed dynamically.  
Refer to dashboard charts.

## 🔹 Frequency Impact (Simplified Model)

| Scenario | ΔP (GW) | Δf (Hz) | Severity |
|---------|----------|---------|----------|
| S1 | 0.1 | –0.005 | Low |
| S2 | 0.4 | –0.020 | Low |
| S3 | 1.0 | –0.050 | Low |
| S4 | 2.0 | –0.100 | Low |
| S5 | 5.0 | –0.250 | Moderate |

---

# 📉 Risk Matrix (Impact × Likelihood)

Computed from voltage, frequency, and loading metrics.

| Scenario | Impact | Likelihood | Risk Score | Risk Level |
|----------|--------|------------|------------|------------|
| S1 | 1 | 1 | 1 | Low |
| S2 | 1 | 2 | 2 | Low |
| S3 | 1 | 3 | 3 | Low |
| S4 | 1 | 4 | 4 | Low–Medium |
| S5 | 1 | 5 | 5 | Low–Medium |

---

# 🔐 IDS Architecture (Three-Layer Model)

## 🟦 Local Inverter IDS
Monitors anomalies in PV behavior and communication.

## 🟧 Feeder/Substation IDS  
Detects coordinated feeder-level anomalies.

## 🟥 Control Center IDS  
Detects wide-area and national-scale attacks.

---

# 🧪 Automated Testing & Validation

To ensure the reliability and robustness of the simulation framework, an automated testing suite was implemented using `pytest`.

## ✔ What is validated
- All attack scenarios (S1–S5 execute successfully  
- Output structure is correct (tuple format)  
- Data types are valid:
  - Detection flag (boolean)  
  - Frequency deviation (numeric)  
  - Minimum voltage (numeric)  
- Physical consistency:
  - Frequency deviation ≥ 0  
  - Voltage remains positive  

## ▶ Run tests locally

```bash
pip install pytest
python -m pytest -v 
```

📌 Example Output

5 passed in 2.69s

🎯 Purpose

This validation layer ensures:

1. Reproducibility
2. Stability across scenarios
3. Early error detection
4. Reliability of simulation outputs

⚡ Quick Smoke Test
```bash
python scripts/smoke_scenarios.py
```
---

# 🛠️ How to Run the Simulation

From the repository root (`repo/`), install dependencies:

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

- [Solar Power Generation Data](https://www.kaggle.com/datasets/anikannal/solar-power-generation-data)
- [Smart Grid Intrusion Detection Dataset](https://www.kaggle.com/datasets/hussainsheikh03/smart-grid-intrusion-detection-dataset)

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
2) Ensure `data/france_sprint3/*.csv` is present in the deployed repo.
3) Verify:
   - `/health` returns `{"status":"ok"}`
   - `/routes` includes websocket route `"/ws"`

## Frontend (Vercel)
1) Open `realtime/index.html`.
2) The WebSocket input is prefilled by default with:
   `wss://inverter-cyberattack-simulation-1.onrender.com/ws`
3) Click **Connect**, choose scenario (S1–S5), then **Apply**.

## New Real-Time 3D Features
- Scenario visual severity mode (S1 -> S5) with stronger colors, thicker affected lines, and dynamic attack zones.
- Animated attack packets and radial shockwave effects from the substation.
- Risk panel with:
  - Live risk assessment
  - Risk matrix reference level (aligned with dashboard table)
- Audio alerts:
  - Distinct per scenario
  - Recorded siren (`realtime/assets/siren.wav`) with fallback synthesis.
- Presentation mode:
  - Fullscreen + reduced HUD opacity for projector visibility.
- Jury overlay:
  - Scenario title/details shown first, then attack starts after the configured delay.

## AI Cyber Assistant (English)
The 3D view includes a built-in AI assistant with:
- Text commands
- Voice commands (SpeechRecognition)
- Spoken replies (SpeechSynthesis)

Examples:
- `connect`
- `disconnect`
- `scenario S4`
- `status`
- `siren test`
- `presentation mode`
- `demo` (toggle demo locked mode)

## Demo Locked Mode
- One-click auto-demo for oral presentation.
- Automatically runs S1 -> S5 (40 seconds each) in a loop.
- Coordinates voice prompt, scenario overlay, and attack launch timing.

## Local Run (Recommended for Rehearsal)
From the project parent directory (one level above `repo/`), run:

```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r repo/requirements.txt
python -m pip install -r repo/backend/requirements.txt
set PYTHONPATH=repo
python -m uvicorn backend.app:app --app-dir repo --host 0.0.0.0 --port 8000
```

Then open:
- Dashboard: `repo/2ASICYA_Dashboard.html`
- Realtime 3D: `repo/realtime/index.html?ws=ws://localhost:8000/ws`

---

## Presentation Quick Start (60 seconds)
1. Start backend (local or Render).
2. Open dashboard and click **LIVE 3D**.
3. Click **Connect** in the 3D page.
4. Use **AI Cyber Assistant (EN)** or **Demo Locked** to run S1 -> S5.
5. Enable **Presentation Mode** for projector-friendly display.

---

# 👥 Team Contributions

- Roy: simulation code, attack scenarios, results.
- Gilles: dashboard, data integration, visualizations.
- Eseoghene: document coordination and synthesis.
- Rasaq: security/IDS, risk matrix.
- Yves: external datasets, dashboard enrichment.
- Gémima: proofreading, consistency, finalization.
