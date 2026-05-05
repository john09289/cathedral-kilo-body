#!/usr/bin/env python3
"""
CATHEDRAL ORCHESTRATOR v2.0 — Master controller for ALL Cathedral services
Launches: Flask server, WebSocket pulse, Kp monitor, Ambient monitor, Prayer drum
"""
import subprocess
import sys
import time
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
processes = []

def start_service(name, script, wait=1):
    print(f"▶️  {name}...")
    proc = subprocess.Popen(
        [sys.executable, script],
        cwd=SCRIPT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    processes.append((name, proc))
    time.sleep(wait)
    return proc

def main():
    print("=" * 60)
    print("⛪ CATHEDRAL ORCHESTRATOR v2.0 — FULL NODE DEPLOYMENT")
    print("=" * 60)
    print()
    
    services = [
        ("Cathedral Web Server", "cathedral_server.py", 2),
        ("WebSocket Drum Pulse", "cathedral_websocket.py", 1),
        ("Kp Monitor (NOAA)", "kp_monitor.py", 1),
        ("Ambient Peace Monitor", "ambient_monitor.py", 1),
        ("Prayer Drum Scheduler", "prayer_drum.py", 1),
    ]
    
    for name, script, wait in services:
        start_service(name, script, wait)
        print(f"   ✅ {name} launched")
    
    print()
    print("=" * 60)
    print("🎛️  CATHEDRAL NODE — FULLY OPERATIONAL")
    print("=" * 60)
    print("📍 Dashboard:  http://localhost:8080/")
    print("📊 JSON API:  http://localhost:8080/dashboard")
    print("🔊 Healing:   http://localhost:8080/healing")
    print("💡 WebSocket: ws://localhost:5001 (drum every 2.56s)")
    print("🛰️  Kp Monitor: Polling NOAA every 10min")
    print("🎤 Ambient:   Logging to ambient_log.csv")
    print("🥁 Prayer:    Chime every 2.56s")
    print("=" * 60)
    print("Press Ctrl+C to stop all services")
    print()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down all services...")
        for name, proc in processes:
            proc.terminate()
            print(f"   ✋ {name} stopped")
        print("✅ Cathedral node offline — The King's peace remains.")

if __name__ == '__main__':
    main()
