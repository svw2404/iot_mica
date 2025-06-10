"""Activity detection model placeholder."""

from dataclasses import dataclass
from typing import Dict


@dataclass
class Activity:
    name: str
    confidence: float


def detect_activity(sensor_data: Dict) -> Activity:
    """Dummy activity detection based on sensor data."""
    if sensor_data.get("motion"):
        return Activity(name="motion", confidence=0.9)
    return Activity(name="idle", confidence=0.5)
