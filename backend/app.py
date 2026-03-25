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
from starlette.routing import WebSocketRoute

# NOTE: This backend is meant to run on Render as a real-time FastAPI WebSocket service.
# It should be started with: `python -m uvicorn backend.app:app --host 0.0.0.0 --port $PORT`

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


@app.get("/routes")
def routes():
    """
    Debug endpoint: tells which websocket/http routes are registered in the deployed app.
    Useful to verify Render deploy configuration.
    """
    ws_routes = []
    http_routes = []
    for r in app.routes:
        if isinstance(r, WebSocketRoute):
            ws_routes.append(r.path)
        else:
            # Starlette route objects may not have methods attribute; guard it.
            path = getattr(r, "path", None)
            methods = getattr(r, "methods", None)
            if path and methods:
                http_routes.append(path)

    return {"http_routes": sorted(set(http_routes)), "websocket_routes": sorted(set(ws_routes))}


@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    await ws.accept()
    try:
        # Let the client know the WebSocket handshake succeeded, then init simulation.
        # This avoids "idle" timeouts on some proxies if simulation init is heavy.
        try:
            await ws.send_text(json.dumps({"type": "info", "message": "ws_accepted"}))
        except Exception:
            pass

        sim = SimulationState()
    except Exception as e:
        # If the simulation can't initialize (missing CSVs, bad paths, etc),
        # tell the client explicitly so it can display the error.
        try:
            await ws.send_text(json.dumps({"type": "error", "error": str(e)}))
        except Exception:
            pass
        try:
            await ws.close(code=1011, reason="Simulation init error")
        except Exception:
            pass
        return

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
    except Exception as e:
        try:
            await ws.send_text(json.dumps({"type": "error", "error": str(e)}))
        except Exception:
            pass
        try:
            await ws.close(code=1011, reason="Simulation error")
        except Exception:
            pass
    finally:
        recv_task.cancel()
