# src/config.py

from dataclasses import dataclass


@dataclass
class SimulationConfig:

    # Time
    start_time: str = "2026-02-04 00:00"
    end_time: str = "2026-02-04 23:45"
    freq: str = "15min"

    # Monte Carlo
    n_runs: int = 50
    seed: int = 42

    # PV parameters
    pv_noise_std: float = 0.05
    load_noise_std: float = 0.03

    # Attack
    attack_time: str = "2026-02-04 12:00"
    attack_multiplier: float = 0.0   # 0 = full inverter shutdown

    # Voltage limits
    v_min_limit: float = 0.95
    v_max_limit: float = 1.05

    # Line overload limit
    max_line_loading: float = 100.0