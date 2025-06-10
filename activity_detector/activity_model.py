"""Activity detection model placeholder."""

from dataclasses import dataclass
from typing import Dict

from utils.logger import get_logger


@dataclass
class Activity:
    name: str
    confidence: float


def detect_activity(sensor_data: Dict) -> Activity:
    """Dummy activity detection based on sensor data."""
    if sensor_data.get("motion"):
        return Activity(name="motion", confidence=0.9)
    return Activity(name="idle", confidence=0.5)


log = get_logger("ActivityModel")


class ActivityModel:
    """Generate activities from incoming sensor events."""

    def __init__(self, bus) -> None:
        self.bus = bus
        self.data: Dict[str, float] = {}
        bus.subscribe("sensor/motion", self._handle_motion)
        bus.subscribe("sensor/temp", self._handle_temp)

    def _handle_motion(self, _topic: str, payload: Dict) -> None:
        self.data["motion"] = payload.get("value")
        self._publish_activity()

    def _handle_temp(self, _topic: str, payload: Dict) -> None:
        self.data["temp"] = payload.get("value")
        self._publish_activity()

    def _publish_activity(self) -> None:
        activity = detect_activity(self.data)
        log.info(f"Activity={activity.name} conf={activity.confidence}")
        self.bus.publish(
            "activity/detected",
            {"activity": activity.name, "confidence": activity.confidence},
        )
