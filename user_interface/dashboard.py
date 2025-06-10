from __future__ import annotations

import threading
from flask import Flask, jsonify

from utils.logger import get_logger


log = get_logger("Dashboard")


class Dashboard(threading.Thread):
    """Simple dashboard exposing latest sensor and activity data via HTTP."""

    def __init__(self, bus, host: str = "0.0.0.0", port: int = 5000) -> None:
        super().__init__(daemon=True)
        self.bus = bus
        self.host = host
        self.port = port
        self.app = Flask(__name__)
        self.state = {"temp": None, "motion": None, "activity": None}
        bus.subscribe("sensor/temp", self._on_temp)
        bus.subscribe("sensor/motion", self._on_motion)
        bus.subscribe("activity/detected", self._on_activity)

        @self.app.route("/")
        def index():  # type: ignore
            return jsonify(self.state)

    def _on_temp(self, _topic: str, payload: dict) -> None:
        self.state["temp"] = payload.get("value")

    def _on_motion(self, _topic: str, payload: dict) -> None:
        self.state["motion"] = payload.get("value")

    def _on_activity(self, _topic: str, payload: dict) -> None:
        self.state["activity"] = payload.get("activity")

    def run(self) -> None:
        log.info("Starting dashboard")
        self.app.run(host=self.host, port=self.port)
