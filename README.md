Cyber-Physical Simulation of Coordinated Attacks on Distributed Solar PV Inverters
Abstract

The rapid integration of distributed photovoltaic (PV) systems into modern power grids introduces new cyber-physical vulnerabilities. This project presents a simulation framework for modeling coordinated cyberattacks on distributed solar inverters within a synthetic French distribution network.

Using time-series power flow analysis in pandapower, the framework evaluates voltage stability, line loading, and frequency deviations under multiple attack scenarios (S1–S5). A quantitative cyber-physical risk assessment is performed, and a three-layer Intrusion Detection System (IDS) architecture is proposed to mitigate coordinated inverter manipulation.

Results indicate that while distribution-level voltage impacts remain limited, large-scale coordinated PV shutdown (≥5 GW) can produce moderate frequency deviations at the system level, highlighting the importance of wide-area monitoring and detection.

1. Introduction

Distributed Energy Resources (DER), particularly grid-connected PV inverters, are increasingly digitized and remotely controllable. While this enhances operational flexibility, it also expands the cyber attack surface of power systems.

This project investigates:

Coordinated inverter shutdown attacks

Cascading cyber-physical effects

Distribution-level electrical impacts

System-level frequency deviations

Risk quantification

IDS-based mitigation strategies

2. System Model
2.1 Distribution Network

The simulated network is based on synthetic French distribution data:

33 buses

37 lines

32 loads

7 aggregated PV generators

15-minute time resolution

All data are synthetic and research-safe.

2.2 Power Flow Simulation

Time-series AC power flow is executed using pandapower.

At each timestep:

Load and PV generation are updated

Attack conditions are applied (if active)

AC power flow is solved

Electrical metrics are recorded

Key monitored variables:

Bus voltage magnitude (p.u.)

Line loading (%)

Total PV generation (MW)

Total load (MW)

3. Cyberattack Model

Five escalating attack scenarios are modeled:

Scenario	Description	PV Loss
S1	Local disturbance	0.1 GW
S2	Feeder-level coordinated attack	0.4 GW
S3	Multi-region attack	1.0 GW
S4	Regional synchronized shutdown	2.0 GW
S5	National-scale coordinated shutdown	5.0 GW

Attack characteristics:

Instantaneous PV disconnection

Trigger time: 12:00

Full inverter shutdown in targeted regions

4. Simulation Results
4.1 Voltage Stability

Maximum observed deviation: −0.003 p.u.

All voltages remained within EN50160 limits (±10%)

No voltage collapse observed

Distribution networks showed strong robustness to PV loss at simulated penetration levels.

4.2 Line Loading

Maximum loading: ~74%

No thermal overload violations

Minimal deviation from baseline conditions

4.3 Frequency Impact (System-Level Approximation)

Assumptions:

100 GW national system size

10% generation loss → 0.5 Hz drop

Scenario	ΔP (GW)	Δf (Hz)
S1	0.1	−0.005
S2	0.4	−0.020
S3	1.0	−0.050
S4	2.0	−0.100
S5	5.0	−0.250

Only S5 produces moderate frequency deviation.

5. Risk Assessment

Cyber-physical risk is computed as:

Risk = Impact × Likelihood

Scenario	Impact	Likelihood	Risk Score	Level
S1	1	3	3	Low
S2	2	3	6	Low–Medium
S3	2	4	8	Medium
S4	3	4	12	High
S5	4	2	8	Medium

Highest risk scenario: S4
Most damaging scenario: S5

6. Intrusion Detection Architecture

A hierarchical three-layer IDS is proposed:

Layer 1 — Local Inverter IDS

Detects abrupt power drops

Monitors repeated command injections

Detects communication anomalies

Layer 2 — Feeder/Substation IDS

Identifies coordinated PV loss

Detects correlated voltage sag

Monitors synchronized inverter behavior

Layer 3 — Control Center IDS

Detects multi-region attacks

Monitors frequency deviation

Aggregates SCADA anomalies

7. Implementation
7.1 Requirements

Python 3.9+

pandapower

numpy

pandas

matplotlib

Install dependencies:

pip install -r requirements.txt
7.2 Execution

Run the main simulation:

python src/main.py

Outputs include:

Voltage time series

Line loading analysis

Monte Carlo risk metrics

Attack scenario comparisons

8. Research Contributions

This project demonstrates:

A reproducible cyber-physical simulation framework

Quantified inverter attack impact

Distribution-level robustness assessment

System-level frequency sensitivity estimation

A layered IDS detection concept

9. Future Work

Dynamic frequency modeling (swing equation)

Protection system interaction modeling

Cascading failure analysis

Realistic communication-layer attack modeling

Integration with hardware-in-the-loop testing
