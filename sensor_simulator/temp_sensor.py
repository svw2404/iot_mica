"""Simulated temperature sensor."""

import random
import threading
import time

from utils.logger import get_logger


log = get_logger("TempSensor")


def read_temperature() -> float:
    """Return a random temperature value in Celsius."""
    return round(random.uniform(15.0, 30.0), 2)


class TempSensor(threading.Thread):
    """Publish temperature readings periodically on the event bus."""

    def __init__(self, bus, interval: int = 5) -> None:
        super().__init__(daemon=True)
        self.bus = bus
        self.interval = interval

    def run(self) -> None:
        while True:
            value = read_temperature()
            log.info(f"Temp={value}")
            self.bus.publish("sensor/temp", {"value": value})
            time.sleep(self.interval)
