# Cyber-Physical Simulation of Coordinated Attacks on Distributed Solar PV Inverters

## Abstract

The rapid integration of distributed photovoltaic (PV) systems into modern power grids introduces new cyber-physical vulnerabilities. This project presents a simulation framework for modeling coordinated cyberattacks targeting distributed solar inverters within a synthetic French distribution network.

Using time-series AC power-flow analysis implemented in **pandapower**, the framework evaluates voltage stability, line loading, and system-level frequency deviations under multiple attack scenarios (S1–S5). A quantitative cyber-physical risk assessment is conducted, and a hierarchical three-layer Intrusion Detection System (IDS) architecture is proposed.

---

## 1. Introduction

This project investigates:

- Coordinated inverter shutdown attacks  
- Cascading cyber-physical effects  
- Distribution-level electrical impacts  
- System-level frequency deviations  
- Risk quantification  
- IDS-based mitigation strategies  

---

## 2. System Model

### 2.1 Distribution Network

The simulated synthetic French network includes:

- 33 buses  
- 37 lines  
- 32 loads  
- 7 aggregated PV generators  
- 15-minute time resolution  

All data are synthetic and research-safe.

---

## 3. Cyberattack Scenarios (S1–S5)

| Scenario | Description | PV Loss (GW) |
|----------|------------|--------------|
| S1 | Local disturbance | 0.1 |
| S2 | Feeder-level coordinated attack | 0.4 |
| S3 | Multi-region attack | 1.0 |
| S4 | Regional synchronized shutdown | 2.0 |
| S5 | National-scale coordinated shutdown | 5.0 |

Attack trigger time: **12:00**  
PV in affected regions is disconnected instantaneously.

---

## 4. Simulation Results

### 4.1 Voltage Stability

- Maximum observed deviation: −0.003 p.u.  
- All voltages remained within EN50160 limits (±10%)  
- No voltage collapse observed  

---

### 4.2 Line Loading

- Maximum loading: ~74%  
- No thermal overload violations  

---

### 4.3 Frequency Impact (System-Level Approximation)

Assumptions:

- 100 GW system size  
- 10% generation loss → 0.5 Hz drop  

| Scenario | ΔP (GW) | Δf (Hz) |
|----------|----------|----------|
| S1 | 0.1 | −0.005 |
| S2 | 0.4 | −0.020 |
| S3 | 1.0 | −0.050 |
| S4 | 2.0 | −0.100 |
| S5 | 5.0 | −0.250 |

Only S5 produces moderate frequency deviation.

---

## 5. Risk Assessment

Risk is computed as:

Risk = Impact × Likelihood

| Scenario | Impact | Likelihood | Risk Score | Level |
|----------|---------|------------|------------|--------|
| S1 | 1 | 3 | 3 | Low |
| S2 | 2 | 3 | 6 | Low–Medium |
| S3 | 2 | 4 | 8 | Medium |
| S4 | 3 | 4 | 12 | High |
| S5 | 4 | 2 | 8 | Medium |

Highest risk scenario: **S4**  
Most damaging scenario: **S5**

---

## 6. IDS Architecture

### Layer 1 — Local Inverter IDS
- Detects abrupt PV drop  
- Monitors repeated command injections  
- Detects communication anomalies  

### Layer 2 — Feeder / Substation IDS
- Identifies coordinated feeder-wide shutdown  
- Detects correlated voltage sag  

### Layer 3 — Control Center IDS
- Detects multi-region attacks  
- Monitors frequency deviation  

---

## 7. Installation

Requirements:

- Python 3.9+
- pandapower
- numpy
- pandas
- matplotlib

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 8. Run Simulation

```bash
python src/main.py
```

Outputs:

- Voltage time series  
- Line loading analysis  
- Risk metrics  
- Scenario comparison  

---

## 9. Future Work

- Dynamic frequency modeling  
- Protection interaction modeling  
- Cascading failure analysis  
- Communication-layer attack modeling  
- Hardware-in-the-loop validation  
