from flask import Flask, jsonify, render_template_string
from threading import Thread

# Enhanced UI using Bootstrap for a more aesthetic design
HTML = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>IoT TAP Protection Demo</title>
  <!-- Auto-refresh every 5 seconds -->
  <meta http-equiv="refresh" content="5">
  <!-- Bootstrap CSS -->
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body { background-color: #f8f9fa; }
    .card {
      margin: 50px auto;
      max-width: 500px;
      box-shadow: 0 4px 6px rgba(0,0,0,0.1);
      border: none;
    }
    .card-header {
      background-color: #343a40;
      color: #fff;
      text-align: center;
    }
    .card-body p {
      font-size: 1.1rem;
    }
    .card-footer {
      text-align: center;
      font-size: 0.9rem;
      color: #666;
    }
  </style>
</head>
<body>
  <div class="card">
    <div class="card-header">
      <h3>Activity-Recognition Protection</h3>
    </div>
    <div class="card-body">
      <p><strong>Last Activity:</strong> {{ activity }}</p>
      <p><strong>Last Action:</strong> {{ action }}</p>
      <p><strong>Decision:</strong> 
        <span class="{% if decision == 'ALLOWED' %}text-success{% else %}text-danger{% endif %}">
          {{ decision }}
        </span>
      </p>
      <p><strong>Temperature:</strong> {{ temp }}°C</p>
      <p><strong>Motion:</strong> {{ motion }}</p>
    </div>
    <div class="card-footer">
      &copy; 歐茗可 - Wireless & Mobile Networks Class - Professor Xu
    </div>
  </div>
</body>
</html>
"""

class Dashboard:
    """Tiny Flask server to visualise system state with enhanced UI."""
    def __init__(self, bus, host="0.0.0.0", port=5000):
        self.bus       = bus
        self._activity = "unknown"
        self._action   = "—"
        self._decision = "—"
        self._temp     = "—"
        self._motion   = "—"

        # Subscribe to system events
        bus.subscribe("sensor/temperature", self._on_temp)
        bus.subscribe("sensor/motion",      self._on_motion)
        bus.subscribe("activity/detected",  self._on_activity)
        bus.subscribe("action/decision",    self._on_decision)

        # Explicit import name to ensure correct module is served
        self.app = Flask('user_interface.app')
        self.app.add_url_rule("/",           endpoint="index",  view_func=self._index)
        self.app.add_url_rule("/api/status", endpoint="status", view_func=self._status)

        # Run Flask in a separate thread with debug off
        self._thread = Thread(
            target=self.app.run,
            kwargs={"host": host, "port": port, "debug": False},
            daemon=True
        )

    def _index(self):
        # Serve the HTML dashboard
        return render_template_string(
            HTML,
            activity=self._activity,
            action=self._action,
            decision=self._decision,
            temp=self._temp,
            motion=self._motion
        )

    def _status(self):
        # Serve JSON status (for AJAX or API checks)
        return jsonify(
            activity=self._activity,
            action=self._action,
            decision=self._decision,
            temp=self._temp,
            motion=self._motion
        )

    def _on_temp(self, _topic, payload):
        self._temp = payload.get("value", "—")

    def _on_motion(self, _topic, payload):
        self._motion = payload.get("value", "—")

    def _on_activity(self, _topic, payload):
        self._activity = payload.get("activity", "unknown")

    def _on_decision(self, _topic, payload):
        self._action   = payload.get("action", "—")
        self._decision = "ALLOWED" if payload.get("allow", False) else "BLOCKED"

    def start(self):
        # Launch the Flask server in background
        self._thread.start()
