"""Simple policy checker."""

from typing import Dict


class PolicyChecker:
    def __init__(self, rules: Dict):
        self.rules = rules

    def check(self, activity: str, confidence: float) -> bool:
        rule = self.rules.get(activity)
        if not rule:
            return False
        return confidence >= rule.get("threshold", 1.0)
