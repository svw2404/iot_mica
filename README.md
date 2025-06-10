# IoT Trigger Action Protection

This project provides a simulated IoT environment with a policy enforcement layer. It demonstrates how sensors generate events, how activities are detected, and how policies enforce actions based on these events.

## Project Structure

- `sensor_simulator/` contains simple sensor simulations.
- `activity_detector/` holds the activity detection logic and rules.
- `policy_engine/` performs policy checks against incoming events.
- `protection_layer/` enforces decisions from the policy engine.
- `user_interface/` provides a minimal example application.
- `utils/` contains shared utilities such as logging and an event bus.
- `docs/` offers additional documentation for setup.

Run `python main.py` to start a sample application.
