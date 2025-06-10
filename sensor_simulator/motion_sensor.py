"""Simulated motion sensor."""

import random


def motion_detected() -> bool:
    """Randomly determine if motion is detected."""
    return random.choice([True, False])
