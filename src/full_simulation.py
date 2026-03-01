"""
RESILIENCE DIFFERENTIATION EXPERIMENT
-------------------------------------

Performs attack severity sweep and computes:
- Collapse probability curve
- Severity comparison
- Resilience comparison

Produces resilience separation between:
- No mitigation
- Mitigation enabled

Author: MSc Cyber-Physical Energy Systems
"""

import numpy as np
import random
import matplotlib.pyplot as plt
from dataclasses import dataclass


# ============================================================
# CONFIGURATION
# ============================================================

@dataclass
class Config:
    n_inverters: int = 20
    sim_time: float = 10.0
    dt: float = 0.01

    attack_start: float = 2.0
    detection_delay: float = 0.6

    trip_threshold: float = 0.80
    reconnect_threshold: float = 0.95

    damping: float = 2.5
    droop_gain: float = 3.5
    recovery_gain: float = 5.0
    coupling_strength: float = 0.8

    cascade_penalty: float = 0.02

    monte_carlo_runs: int = 150


CFG = Config()


# ============================================================
# CORE SIMULATION
# ============================================================

def run_simulation(attack_magnitude, mitigate=False, seed=None):

    if seed is not None:
        np.random.seed(seed)

    steps = int(CFG.sim_time / CFG.dt)
    time = np.linspace(0, CFG.sim_time, steps)

    voltages = np.ones((CFG.n_inverters, steps))
    active = np.ones(CFG.n_inverters)

    detected = False
    attack_state = 0.0

    for t in range(1, steps):
        current_time = time[t]

        attack_input = 0.0
        if current_time >= CFG.attack_start:
            attack_input = attack_magnitude

        # filtered attack
        attack_state += (attack_input - attack_state) * CFG.dt / 0.2

        if (not detected and
                current_time >= CFG.attack_start + CFG.detection_delay):
            detected = True

        avg_voltage = np.mean(voltages[:, t - 1])

        for i in range(CFG.n_inverters):

            if active[i] == 0:
                if mitigate and detected and avg_voltage > CFG.reconnect_threshold:
                    active[i] = 1
                else:
                    voltages[i, t] = 0
                    continue

            V = voltages[i, t - 1]

            droop = CFG.droop_gain * (1 - V)
            coupling = CFG.coupling_strength * (avg_voltage - V)

            effective_attack = attack_state
            recovery = 0
            damping = CFG.damping

            if mitigate and detected:
                effective_attack *= 0.4
                recovery = CFG.recovery_gain * (1 - V)
                damping *= 1.3

            dV = (
                -damping * (V - 1)
                - effective_attack
                + droop
                + coupling
                + recovery
                + np.random.normal(0, 0.0015)
            )

            voltages[i, t] = V + dV * CFG.dt

            if voltages[i, t] < CFG.trip_threshold:
                active[i] = 0
                voltages[i, t] = 0

        if np.sum(active) < CFG.n_inverters * 0.5:
            voltages[:, t] -= CFG.cascade_penalty

    tripped = CFG.n_inverters - np.sum(active)
    collapse = np.sum(active) < CFG.n_inverters * 0.3

    max_dev = np.max(np.abs(voltages - 1))
    severity = max_dev + (tripped / CFG.n_inverters)
    resilience = 1 / (1 + severity)

    return collapse, severity, resilience


# ============================================================
# RESILIENCE SWEEP
# ============================================================

def resilience_sweep():

    attack_range = np.linspace(0.2, 0.8, 12)

    collapse_no = []
    collapse_mit = []

    for attack in attack_range:

        col_no = 0
        col_mit = 0

        for run in range(CFG.monte_carlo_runs):

            c1, _, _ = run_simulation(attack, False, seed=run)
            c2, _, _ = run_simulation(attack, True, seed=run)

            if c1:
                col_no += 1
            if c2:
                col_mit += 1

        collapse_no.append(col_no / CFG.monte_carlo_runs)
        collapse_mit.append(col_mit / CFG.monte_carlo_runs)

        print(f"Attack {attack:.2f} | NoMit: {collapse_no[-1]:.2f} | Mit: {collapse_mit[-1]:.2f}")

    return attack_range, collapse_no, collapse_mit


# ============================================================
# PLOT RESULTS
# ============================================================

def plot_results(attack_range, collapse_no, collapse_mit):

    plt.figure(figsize=(8, 5))
    plt.plot(attack_range, collapse_no, marker='o')
    plt.plot(attack_range, collapse_mit, marker='s')
    plt.xlabel("Attack Magnitude")
    plt.ylabel("Collapse Probability")
    plt.title("Resilience Differentiation Curve")
    plt.legend(["No Mitigation", "Mitigation Enabled"])
    plt.grid(True)
    plt.show()


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print("\nRunning Resilience Differentiation Study...\n")

    attack_range, collapse_no, collapse_mit = resilience_sweep()

    plot_results(attack_range, collapse_no, collapse_mit)

    print("\nStudy Complete.")