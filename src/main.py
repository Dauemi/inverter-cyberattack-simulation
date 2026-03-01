# src/main.py

import logging
from src.config import SimulationConfig
from src.full_simulation import FullGridSimulation


def main():

    logging.basicConfig(level=logging.INFO)

    config = SimulationConfig()
    sim = FullGridSimulation(config)

    logging.info("Running full AC cyber-physical grid simulation...")

    # Single detailed run
    df, cascades = sim.run_single_simulation()

    # Monte Carlo
    mc_results = sim.run_monte_carlo()

    print("\n===== FINAL RESULTS =====")
    print("Average Undervoltage %:",
          round(mc_results["undervoltage_%"].mean(), 2))
    print("Average Overvoltage %:",
          round(mc_results["overvoltage_%"].mean(), 2))
    print("Average Line Overload %:",
          round(mc_results["line_overload_%"].mean(), 2))
    print("Average Cascade Events:",
          round(mc_results["cascade_events"].mean(), 2))

    # Professional plots
    sim.plot_professional_results(df)
    sim.plot_monte_carlo_distribution(mc_results)


if __name__ == "__main__":
    main()