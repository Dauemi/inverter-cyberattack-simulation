2ASICYA – Sprint 3 Synthetic Datasets (France-Representative)

IMPORTANT:
- These datasets are SYNTHETIC and for academic simulation purposes.
- They are NOT real operational data from RTE, Enedis, or any inverter manufacturer.
- Designed for Sprint 3 (Digital Twin setup) and reproducible simulations.

Files:
1) fr_grid_buses.csv
2) fr_grid_lines.csv
3) fr_grid_loads.csv
4) fr_grid_pv_generators.csv
5) fr_grid_metadata.json
6) fr_load_profile_15min.csv
7) fr_inverter_parameters.csv
8) fr_attack_scenarios_S1_S5.csv

Suggested use:
- Build baseline powerflow with peak loads scaled by fr_load_profile_15min.csv multiplier.
- Model PV generators using fr_grid_pv_generators.csv and inverter classes from fr_inverter_parameters.csv.
- Prepare event hooks using fr_attack_scenarios_S1_S5.csv (Sprint 4 executes full scenarios).
