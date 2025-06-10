"""Simple command-line interface."""

from sensor_simulator import temp_sensor, motion_sensor
from activity_detector import activity_model
from policy_engine import policy_checker
from protection_layer import enforcement
import json
import threading
from flask import Flask, jsonify


def load_rules(path: str):
    with open(path) as fh:
        return json.load(fh)


def main():
    rules = load_rules("policy_engine/policy_rules.json")
    checker = policy_checker.PolicyChecker(rules)

    temp = temp_sensor.read_temperature()
    motion = motion_sensor.motion_detected()
    activity = activity_model.detect_activity({"motion": motion})

    if checker.check(activity.name, activity.confidence):
        enforcement.enforce(activity.name, {"temp": temp})
    else:
        print("Policy blocked action")


class Dashboard:
    """Minimal Flask dashboard streaming sensor data."""

    def __init__(self, bus, host: str = "0.0.0.0", port: int = 5000) -> None:
        self.bus = bus
        self.host = host
        self.port = port
        self.app = Flask(__name__)
        self.data = {"temp": None, "motion": None}
        self.app.add_url_rule("/", "index", self._index)

    def _index(self):
        return jsonify(self.data)

    # Event handlers -----------------------------------------------------
    def _handle_temp(self, _topic, payload):
        self.data["temp"] = payload.get("value")

    def _handle_motion(self, _topic, payload):
        self.data["motion"] = payload.get("value")

    def start(self) -> threading.Thread:
        """Start the Flask server in a background thread."""
        self.bus.subscribe("sensor/temp", self._handle_temp)
        self.bus.subscribe("sensor/motion", self._handle_motion)
        thread = threading.Thread(
            target=self.app.run,
            kwargs={
                "host": self.host,
                "port": self.port,
                "use_reloader": False,
                "debug": False,
            },
            daemon=True,
        )
        thread.start()
        self.thread = thread
        return thread


if __name__ == "__main__":
    main()
