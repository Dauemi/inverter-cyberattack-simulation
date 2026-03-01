
---

## 🎯 Project Objective
![ECE Paris](https://img.shields.io/badge/ECE%20Paris-Cyber%20Physical%20Systems-003366)
![Smart Grid Security](https://img.shields.io/badge/Smart%20Grid-Security-red)
![pandapower](https://img.shields.io/badge/Simulation-pandapower-success)
![Monte Carlo](https://img.shields.io/badge/Analysis-Time%20Series-blueviolet)
![License MIT](https://img.shields.io/badge/License-MIT-yellow)

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

# 📊 Key Results

## 🔹 Voltage Stability
Across all scenarios S1–S5:

- Worst ΔV observed: **–0.003 p.u.**  
- Voltage remained within **EN50160 standards (±10%)**

Even S5 caused negligible voltage instability.

---

## 🔹 Line Loading
Line loading differences were extremely small:

- Max line loading: **~74%** (no overloads)
- Δ loading between base and attack: **0.0%** in all cases

No thermal limits were exceeded.

---

## 🔹 Frequency Impact (Simplified Model)

Using:
- System size: 100 GW  
- Sensitivity: 10% loss → 0.5 Hz drop  

| Scenario | ΔP (GW) | Δf (Hz) | Severity |
|---------|----------|----------|-----------|
| S1 | 0.1 | –0.005 | Low |
| S2 | 0.4 | –0.020 | Low |
| S3 | 1.0 | –0.050 | Low |
| S4 | 2.0 | –0.100 | Low |
| **S5** | 5.0 | –0.250 | Moderate |

Only S5 reaches **moderate** system impact.

---

# 📉 Risk Matrix (Impact × Likelihood)

| Scenario | Impact | Likelihood | Risk Score | Risk Level |
|----------|---------|------------|------------|-------------|
| **S1** | 1 | 3 | 3 | Low |
| **S2** | 2 | 3 | 6 | Low–Medium |
| **S3** | 2 | 4 | 8 | Medium |
| **S4** | 3 | 4 | 12 | High |
| **S5** | 4 | 2 | 8 | Medium |

Highest-risk scenario: **S4 (High)**  
Most damaging scenario: **S5 (Moderate, but large ΔP)**

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
