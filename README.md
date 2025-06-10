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

## Quick start
1. Install dependencies: `pip install -r requirements.txt`
2. Run the application: `python main.py`
   - Terminal will stream sensor/activity/policy logs
   - You’ll also see:
     ```
      * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
     ```
3. Open your browser at <http://localhost:5000> to view the live dashboard.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
