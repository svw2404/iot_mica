"""Policy checker used to approve or block detected activities."""

from __future__ import annotations

import json
from typing import Any, Dict, Optional

from utils.event_bus import EventBus


class PolicyChecker:
    """Validate activities against policy thresholds."""

    def __init__(
        self,
        bus: Optional[EventBus] = None,
        rules: Optional[Dict[str, Dict[str, Any]]] = None,
        rules_path: str = "policy_engine/policy_rules.json",
    ) -> None:
        """Create a new ``PolicyChecker``.

        Parameters
        ----------
        bus:
            ``EventBus`` used to subscribe to activity events. If ``None`` the
            checker works as a simple helper without bus integration.
        rules:
            Optional rules dictionary. If omitted ``rules_path`` will be loaded
            instead.
        rules_path:
            Path to a JSON rules file. Ignored when ``rules`` is provided.
        """

        self.bus = bus
        self.rules: Dict[str, Dict[str, Any]] = (
            rules if rules is not None else self._load_rules(rules_path)
        )

        if self.bus is not None:
            self.bus.subscribe("activity/detected", self._on_activity)

    # ------------------------------------------------------------------
    def _load_rules(self, path: str) -> Dict[str, Dict[str, Any]]:
        """Load policy rules from ``path``.

        The JSON may optionally wrap the actual policies in a top-level
        ``"policies"`` key. Each policy must contain a numeric ``threshold``
        value.
        """

        with open(path) as fh:
            data = json.load(fh)

        if "policies" in data and isinstance(data["policies"], dict):
            data = data["policies"]

        rules: Dict[str, Dict[str, Any]] = {}
        for act, rule in data.items():
            threshold = rule.get("threshold")
            if not isinstance(threshold, (int, float)):
                raise ValueError(f"Policy for '{act}' missing numeric 'threshold'")
            rules[act] = {"threshold": float(threshold)}
        return rules

    # ------------------------------------------------------------------
    def _on_activity(self, _topic: str, payload: Dict[str, Any]) -> None:
        activity = payload.get("activity")
        confidence = payload.get("confidence", 0.0)
        if self.check(activity, confidence):
            self.bus.publish("policy/allowed", payload)
        else:
            self.bus.publish("policy/blocked", payload)

    # ------------------------------------------------------------------
    def check(self, activity: str, confidence: float) -> bool:
        rule = self.rules.get(activity)
        if not rule:
            return False
        return confidence >= rule["threshold"]
