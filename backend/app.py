import asyncio
import json
import math
import os
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
import pandapower as pp
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.grid_topology.load_france_grid import load_france_grid
from src.load_data.load_profile_fr import load_fr_load_profile
from src.attacks.attack_fr import apply_attack_to_pv

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def pv_shape_from_timestamp(ts: pd.Timestamp) -> float:
    hour = ts.hour + ts.minute / 60.0
    if hour <= 6 or hour >= 18:
        return 0.0
    x = (hour - 6) / 12.0 * math.pi
    return max(0.0, min(1.0, math.sin(x)))


class SimulationState:
    def __init__(self):
        self.net = load_france_grid()
        self.base_load = self.net.load["p_mw"].copy()
        self.base_pv = self.net.sgen["p_mw"].copy()
        self.profile = load_fr_load_profile()
        self.idx = 0
        self.scenario = "S3"
        self.attack_time = pd.to_datetime("2026-02-04 12:00:00")
        self.attack_applied = False
        self.fleet_multiplier = 1.0

    def set_scenario(self, scenario: str) -> None:
        self.scenario = scenario
        self.attack_applied = False
        self.fleet_multiplier = 1.0

    def step(self) -> dict:
        row = self.profile.iloc[self.idx]
        ts = row["timestamp"]
        mult = row["load_multiplier"]

        self.net.load["p_mw"] = self.base_load * mult

        if (not self.attack_applied) and (ts == self.attack_time):
            self.fleet_multiplier = apply_attack_to_pv(self.net, self.scenario)
            self.attack_applied = True

        pv_shape = pv_shape_from_timestamp(ts)
        self.net.sgen["p_mw"] = self.base_pv * pv_shape * self.fleet_multiplier

        pp.runpp(self.net, numba=False)

        buses = []
        for i, row in self.net.bus.iterrows():
            buses.append(
                {
                    "bus_id": int(i + 1),
                    "name": row["name"],
                    "vm_pu": float(self.net.res_bus.loc[i, "vm_pu"]),
                }
            )

        lines = []
        for i, row in self.net.line.iterrows():
            lines.append(
                {
                    "from_bus": int(row["from_bus"]) + 1,
                    "to_bus": int(row["to_bus"]) + 1,
                    "loading": float(self.net.res_line.loc[i, "loading_percent"]),
                }
            )

        payload = {
            "timestamp": ts.strftime("%Y-%m-%d %H:%M:%S"),
            "scenario": self.scenario,
            "attack_applied": self.attack_applied and (ts == self.attack_time),
            "stats": {
                "min_vm": float(self.net.res_bus["vm_pu"].min()),
                "max_vm": float(self.net.res_bus["vm_pu"].max()),
                "max_line_loading": float(self.net.res_line["loading_percent"].max()),
            },
            "buses": buses,
            "lines": lines,
        }

        self.idx = (self.idx + 1) % len(self.profile)
        return payload


@app.get("/health")
def health():
    return {"status": "ok"}


@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    await ws.accept()
    sim = SimulationState()

    async def receiver():
        while True:
            msg = await ws.receive_text()
            try:
                data = json.loads(msg)
                if data.get("type") == "set_scenario":
                    sim.set_scenario(data.get("scenario", "S3"))
            except Exception:
                continue

    recv_task = asyncio.create_task(receiver())

    try:
        while True:
            payload = sim.step()
            await ws.send_text(json.dumps(payload))
            await asyncio.sleep(1.0)
    except Exception:
        pass
    finally:
        recv_task.cancel()
