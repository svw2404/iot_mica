"""Simple command-line interface."""

from sensor_simulator import temp_sensor, motion_sensor
from activity_detector import activity_model
from policy_engine import policy_checker
from protection_layer import enforcement
import json


def load_rules(path: str):
    with open(path) as fh:
        return json.load(fh)


def main():
    rules = load_rules("policy_engine/policy_rules.json")
    checker = policy_checker.PolicyChecker(rules)

    temp = temp_sensor.read_temperature()
    motion = motion_sensor.motion_detected()
    activity = activity_model.detect_activity({"motion": motion})

    if checker.check(activity.name, activity.confidence):
        enforcement.enforce(activity.name, {"temp": temp})
    else:
        print("Policy blocked action")


if __name__ == "__main__":
    main()
