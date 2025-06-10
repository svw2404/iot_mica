import json
from pathlib import Path

from utils.logger import get_logger

log = get_logger("PolicyChecker")


class PolicyChecker:
    """Maps (current_activity, requested_action) → allow / block."""

    def __init__(self, bus, rules_path: str | Path | None = None) -> None:
        self.bus = bus
        rules_path = rules_path or Path(__file__).with_name("policy_rules.json")
        self.rules = json.loads(Path(rules_path).read_text())["policies"]
        self.current_activity: str | None = None

        bus.subscribe("activity/detected", self._on_activity)
        bus.subscribe("action/requested", self._on_action_request)

    # ─────────────────────────── callbacks ───
    def _on_activity(self, _topic: str, payload: dict) -> None:
        self.current_activity = payload["activity"]
        log.info(f"Context = {self.current_activity}")

    def _on_action_request(self, _topic: str, payload: dict) -> None:
        action = payload["action"]
        allowed = self._is_allowed(action)
        decision = "allow" if allowed else "block"
        log.info(f"Policy ➔ {decision.upper()} {action}")
        self.bus.publish("action/decision", {"action": action, "allow": allowed})

    # ─────────────────────────── internal ───
    def _is_allowed(self, action: str) -> bool:
        if self.current_activity is None:
            return True  # fail-open by default
        for pol in self.rules:
            if pol["activity"] == self.current_activity:
                if action in pol.get("blocked_actions", []):
                    return False
                if action in pol.get("allowed_actions", []):
                    return True
        return True  # undefined ⇒ allow
