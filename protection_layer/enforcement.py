"""Policy enforcement layer."""

from __future__ import annotations

from typing import Dict

from utils.logger import get_logger


log = get_logger("Enforcement")


def enforce(action: str, data: Dict) -> None:
    """Placeholder enforcement routine."""
    print(f"Enforcing action: {action} with data: {data}")


class Enforcement:
    """Subscribe to allowed actions and enforce them."""

    def __init__(self, bus) -> None:
        self.bus = bus
        bus.subscribe("action/allowed", self._handle_allowed)
        bus.subscribe("action/blocked", self._handle_blocked)

    def _handle_allowed(self, _topic: str, payload: Dict) -> None:
        log.info(f"Enforcing {payload['action']}")
        enforce(payload["action"], payload)
        # notify other components of the decision
        self.bus.publish(
            "action/decision",
            {"action": payload.get("action"), "allow": True},
        )

    def _handle_blocked(self, _topic: str, payload: Dict) -> None:
        log.info(f"Blocked {payload['action']}")
        self.bus.publish(
            "action/decision",
            {"action": payload.get("action"), "allow": False},
        )
