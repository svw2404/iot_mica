import time

from utils.event_bus import EventBus
from sensor_simulator.temp_sensor import TempSensor
from sensor_simulator.motion_sensor import MotionSensor
from user_interface.app import Dashboard


def test_temp_sensor_publishes():
    bus = EventBus()
    events = []
    bus.subscribe("sensor/temp", lambda t, p: events.append(p))
    sensor = TempSensor(bus, interval=0.1)
    sensor.start()
    time.sleep(0.2)
    assert events, "TempSensor did not publish any events"


def test_motion_sensor_publishes():
    bus = EventBus()
    events = []
    bus.subscribe("sensor/motion", lambda t, p: events.append(p))
    sensor = MotionSensor(bus, interval=0.1)
    sensor.start()
    time.sleep(0.2)
    assert events, "MotionSensor did not publish any events"


def test_dashboard_start():
    bus = EventBus()
    dash = Dashboard(bus, port=5050)
    thread = dash.start()
    time.sleep(0.1)
    assert thread.is_alive()
