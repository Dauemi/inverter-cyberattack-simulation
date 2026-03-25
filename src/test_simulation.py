import pytest
import numpy as np

from src.full_simulation import run_simulation


@pytest.mark.parametrize(
    "scenario_name, attack_magnitude",
    [
        ("S1", 0.1),
        ("S2", 0.2),
        ("S3", 0.4),
        ("S4", 0.7),
        ("S5", 1.0),
    ],
)
def test_scenarios_run_without_error(scenario_name, attack_magnitude):
    results = run_simulation(attack_magnitude)

    assert results is not None, f"{scenario_name} returned no results"
    assert isinstance(results, tuple), f"{scenario_name} should return a tuple"
    assert len(results) == 3, f"{scenario_name} should return 3 values"

    detected, max_freq_dev, min_voltage = results

    assert isinstance(detected, (bool, np.bool_)), (
        f"{scenario_name} detected flag should be boolean"
    )
    assert isinstance(max_freq_dev, (float, np.floating)), (
        f"{scenario_name} max_freq_dev should be numeric"
    )
    assert isinstance(min_voltage, (float, np.floating)), (
        f"{scenario_name} min_voltage should be numeric"
    )

    assert max_freq_dev >= 0, f"{scenario_name} max_freq_dev should be non-negative"
    assert min_voltage > 0, f"{scenario_name} min_voltage should be positive"