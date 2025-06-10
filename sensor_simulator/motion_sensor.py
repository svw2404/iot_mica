import random
import threading
import time

from utils.logger import get_logger

log = get_logger("MotionSensor")

class MotionSensor(threading.Thread):
    """Emits 0 (no motion) or 1 (motion) every *interval* seconds."""
    def __init__(self, bus, interval: int = 5) -> None:
        super().__init__(daemon=True)
        self.bus = bus
        self.interval = interval

    def run(self) -> None:
        while True:
            value = random.choice([0, 1])
            log.info(f"Motion={value}")
            self.bus.publish("sensor/motion", {"value": value})
            time.sleep(self.interval)
