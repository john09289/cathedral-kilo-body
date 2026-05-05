#!/usr/bin/env python3
"""
Kp-INDEX MONITOR — Tracks Enemy atmospheric jamming
Fetches real-time planetary K-index from NOAA SWPC.
"""
import requests
import time
import json
import datetime

NOAA_KP_URL = "https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json"

def get_kp_index():
    """Fetch latest Kp index from NOAA."""
    try:
        resp = requests.get(NOAA_KP_URL, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            # Last entry is most recent: [timestamp, kp, a_index, ...]
            latest = data[-1]
            kp = float(latest[1])
            return {
                "kp": kp,
                "timestamp": latest[0],
                "source": "NOAA SWPC",
                "jamming_level": "HIGH" if kp >= 5 else "LOW"
            }
    except Exception as e:
        return {"error": str(e)}
    return {"error": "no data"}

def monitor_loop(interval_minutes=10):
    """Continuously monitor Kp index."""
    print("=" * 50)
    print("📡 Kp-INDEX MONITOR — ENEMY JAMMING DETECTOR")
    print("=" * 50)
    print(f"Source: {NOAA_KP_URL}")
    print(f"Interval: {interval_minutes} minutes")
    print("=" * 50)
    
    while True:
        result = get_kp_index()
        now = datetime.datetime.utcnow().isoformat() + "Z"
        
        if "kp" in result:
            kp = result["kp"]
            jamming = "🔴 JAMMING HIGH" if kp >= 5 else "🟢 CLEAN"
            print(f"[{now}] Kp: {kp:.1f} | {jamming}")
            
            # Log to file
            log_entry = {
                "timestamp": now,
                "kp": kp,
                "jamming_level": result["jamming_level"]
            }
            with open("kp_log.jsonl", "a") as f:
                f.write(json.dumps(log_entry) + "\n")
        else:
            print(f"[{now}] ERROR: {result.get('error', 'unknown')}")
        
        time.sleep(interval_minutes * 60)

if __name__ == '__main__':
    try:
        monitor_loop(10)  # check every 10 minutes
    except KeyboardInterrupt:
        print("\n🛑 Kp monitor stopped")
