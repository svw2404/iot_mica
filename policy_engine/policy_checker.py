"""Simple policy checker subscribed to the event bus."""

from __future__ import annotations

import json
from typing import Dict

from utils.logger import get_logger


log = get_logger("PolicyChecker")


class PolicyChecker:
    def __init__(self, bus, rules_path: str = "policy_engine/policy_rules.json") -> None:
        self.bus = bus
        self.rules = self._load_rules(rules_path)
        self.current_activity: Dict | None = None
        bus.subscribe("activity/detected", self._handle_activity)
        bus.subscribe("action/requested", self._handle_request)

    def _load_rules(self, path: str) -> Dict:
        with open(path) as fh:
            return json.load(fh)

    def _handle_activity(self, _topic: str, payload: Dict) -> None:
        self.current_activity = payload

    def _handle_request(self, _topic: str, payload: Dict) -> None:
        act = self.current_activity or {"activity": "idle", "confidence": 0.0}
        allowed = self.check(act["activity"], act["confidence"])
        topic = "action/allowed" if allowed else "action/blocked"
        log.info(f"{topic}: {payload['action']}")
        self.bus.publish(topic, payload)
        # emit a generic decision event for UI updates and auditing
        self.bus.publish(
            "action/decision",
            {"action": payload.get("action"), "allow": allowed},
        )

    def check(self, activity: str, confidence: float) -> bool:
        rule = self.rules.get(activity)
        if not rule:
            return False
        return confidence >= rule.get("threshold", 1.0)
