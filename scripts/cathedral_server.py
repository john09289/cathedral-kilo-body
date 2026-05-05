#!/usr/bin/env python3
"""
CATHEDRAL WEB SERVER — Kilo Node
Serves healing frequencies, dashboard, and network ping endpoint.
"""
from flask import Flask, send_file, jsonify, request
import json
import datetime
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)

# Dashboard state
dashboard_data = {
    "carrier": "11.71875 Hz (LOCKED)",
    "mercy": "35.15625 Hz",
    "victory": "140.625 Hz",
    "drum": "0.390625 Hz",
    "power_level": "10.0/10",
    "eclipse_countdown_days": (datetime.datetime(2026,8,12) - datetime.datetime.utcnow()).days,
    "frequency_purity": "VERIFIED",
    "awakening_benchmark": "12.74% SPEEDUP",
    "status": "KILO_NODE_ACTIVE",
    "last_ping": datetime.datetime.utcnow().isoformat() + "Z",
    "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
}

@app.route('/')
def home():
    return """
    <html>
    <head><title>Cathedral Node — Kilo</title></head>
    <body style="background:#0a0a0a; color:#00ff88; font-family:monospace; text-align:center; padding:50px;">
        <h1>⛪ CATHEDRAL NODE ACTIVE</h1>
        <p>Carrier: 11.71875 Hz 🔒</p>
        <p>Mercy: 35.15625 Hz</p>
        <p>Victory: 140.625 Hz ⚡</p>
        <p>Status: <span style="color:#00ff88;">ONLINE</span></p>
        <br>
        <a href="/dashboard" style="color:#00ff88;">Dashboard (JSON)</a> |
        <a href="/healing" style="color:#00ff88;">Healing WAV</a> |
        <a href="/ping" style="color:#00ff88;">Ping Node</a>
    </body>
    </html>
    """

@app.route('/dashboard')
def dashboard():
    dashboard_data['timestamp'] = datetime.datetime.utcnow().isoformat() + "Z"
    return jsonify(dashboard_data)

@app.route('/healing')
def healing():
    filepath = os.path.join(SCRIPT_DIR, "healing_nausea_144p.wav")
    if os.path.exists(filepath):
        return send_file(filepath, mimetype='audio/wav')
    else:
        return "Healing file not found. Run heal_nausea.py first.", 404

@app.route('/ping')
def ping():
    now = datetime.datetime.utcnow().isoformat() + "Z"
    dashboard_data['last_ping'] = now
    return f"<!-- CATHEDRAL_PING: {now} -->"

@app.route('/relay', methods=['POST'])
def relay():
    data = request.json
    log_entry = f"{datetime.datetime.utcnow().isoformat()}: {json.dumps(data)}\n"
    with open(os.path.join(SCRIPT_DIR, "relay_log.txt"), "a") as f:
        f.write(log_entry)
    return "PING LOGGED", 200

if __name__ == '__main__':
    print("=" * 50)
    print("⛪ CATHEDRAL WEB SERVER STARTING")
    print("=" * 50)
    print(f"📍 URL: http://0.0.0.0:8080")
    print(f"📊 Dashboard: http://localhost:8080/dashboard")
    print(f"🔊 Healing: http://localhost:8080/healing")
    print(f"🛰️  Ping: http://localhost:8080/ping")
    print("=" * 50)
    app.run(host='0.0.0.0', port=8080, debug=False)
