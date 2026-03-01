import pandas as pd
import pandapower as pp

def load_france_grid():
    base = "data/france_sprint3/"

    # Load CSV files
    buses = pd.read_csv(base + "fr_grid_buses.csv")
    lines = pd.read_csv(base + "fr_grid_lines.csv")
    loads = pd.read_csv(base + "fr_grid_loads.csv")
    pv = pd.read_csv(base + "fr_grid_pv_generators.csv")

    # Create empty pandapower network
    net = pp.create_empty_network()

    # --- Add buses, keep a map from bus_id -> pandapower index ---
    bus_id_to_pp = {}
    for _, row in buses.iterrows():
        pp_bus_idx = pp.create_bus(
            net,
            vn_kv=row["base_kv"],      # column is base_kv, not vn_kv
            name=row["name"]
        )
        bus_id_to_pp[row["bus_id"]] = pp_bus_idx

    # --- Slack bus: choose the one with type == 'slack' ---
    slack_rows = buses[buses["type"] == "slack"]
    if not slack_rows.empty:
        slack_bus_id = slack_rows.iloc[0]["bus_id"]
        slack_pp_bus = bus_id_to_pp[slack_bus_id]
    else:
        # fallback: use first bus
        slack_pp_bus = list(bus_id_to_pp.values())[0]

    pp.create_ext_grid(
        net,
        bus=slack_pp_bus,
        vm_pu=1.0,
        name="Slack"
    )

    # --- Add lines ---
    for _, row in lines.iterrows():
        from_bus_pp = bus_id_to_pp[row["from_bus"]]
        to_bus_pp = bus_id_to_pp[row["to_bus"]]

        pp.create_line_from_parameters(
            net,
            from_bus=from_bus_pp,
            to_bus=to_bus_pp,
            length_km=row["length_km"],
            r_ohm_per_km=row["r_ohm_per_km"],
            x_ohm_per_km=row["x_ohm_per_km"],
            c_nf_per_km=0.0,          # not in CSV, set 0 for now
            max_i_ka=row["max_i_ka"],
            name=f"LINE_{int(row['line_id'])}"
        )

    # --- Add loads (static baseline load) ---
    for _, row in loads.iterrows():
        bus_pp = bus_id_to_pp[row["bus_id"]]
        pp.create_load(
            net,
            bus=bus_pp,
            p_mw=row["p_mw_peak"],
            q_mvar=row["q_mvar_peak"],
            name=f"LOAD_{int(row['load_id'])}"
        )

    # --- Add PV generators (Sgen) ---
    for _, row in pv.iterrows():
        bus_pp = bus_id_to_pp[row["bus_id"]]
        pp.create_sgen(
            net,
            bus=bus_pp,
            p_mw=row["p_mw_rated"],
            q_mvar=row["q_mvar_cap"],
            name=row["name"]
        )

    return net