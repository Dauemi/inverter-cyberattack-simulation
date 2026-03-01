# src/attacks/shutdown_attack.py

import numpy as np
import pandas as pd


class ScenarioShutdownAttack:
    def __init__(self, multiplier: float, ramp_minutes: int):
        self.multiplier = multiplier
        self.ramp_minutes = ramp_minutes

    def run(self, config):
        np.random.seed(config.seed)

        # Create time index
        time_index = pd.date_range(
            start=config.start_time,
            end=config.end_time,
            freq=config.freq,
        )

        # Random attack time inside simulation window
        attack_time = np.random.choice(time_index)

        print(f"Attack time: {attack_time}")

        # Base load & PV
        load = 1.0 + np.random.normal(0, config.load_noise_std, len(time_index))
        pv = (
            config.pv_penetration
            * (0.8 + np.random.normal(0, config.pv_noise_std, len(time_index)))
        )

        # Apply attack (PV shutdown)
        pv_series = pd.Series(pv, index=time_index)

        pv_series.loc[attack_time:] *= self.multiplier

        # Simple voltage proxy model
        voltage = 1.0 + 0.05 * (pv_series - load)

        df = pd.DataFrame(
            {
                "load": load,
                "pv": pv_series,
                "voltage": voltage,
            },
            index=time_index,
        )

        return df