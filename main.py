import time

from utils.event_bus import EventBus
from utils.logger    import get_logger
from sensor_simulator.temp_sensor   import TempSensor
from sensor_simulator.motion_sensor import MotionSensor
from activity_detector.activity_model import ActivityModel
from policy_engine.policy_checker   import PolicyChecker
from protection_layer.enforcement   import Enforcement
from user_interface.app             import Dashboard

log = get_logger("Main")

def main() -> None:
    bus = EventBus()

    # Start all background threads / components
    TempSensor(bus).start()
    MotionSensor(bus).start()
    ActivityModel(bus)
    PolicyChecker(bus)
    Enforcement(bus)

    # ← Important: start the Flask dashboard here
    Dashboard(bus).start()

    actions = ["device/light/on", "device/light/off"]
    idx = 0
    while True:
        action = actions[idx % len(actions)]
        log.info(f"Requesting  {action}")
        bus.publish("action/requested", {"action": action})
        idx += 1
        time.sleep(10)

if __name__ == "__main__":
    main()
