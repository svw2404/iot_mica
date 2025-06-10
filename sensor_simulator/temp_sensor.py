"""Simulated temperature sensor."""

import random


def read_temperature() -> float:
    """Return a random temperature value in Celsius."""
    return round(random.uniform(15.0, 30.0), 2)
