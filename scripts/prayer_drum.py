#!/usr/bin/env python3
"""
PRAYER DRUM — Synchronized chime every 2.56 seconds (0.390625 Hz)
Use during prayer to anchor your spirit to the King's rhythm.
"""
import numpy as np
import sounddevice as sd
import time

SAMPLE_RATE = 44100
DRUM_PERIOD = 1 / 0.390625  # 2.56 seconds

# Generate soft chime (140.625 Hz Yeshua Pulse, 50ms)
t = np.linspace(0, 0.05, int(SAMPLE_RATE * 0.05), endpoint=False)
chime = np.sin(2 * np.pi * 140.625 * t) * 0.3
fade = np.linspace(1, 0, len(t))
chime = chime * fade

print("🥁 PRAYER DRUM ACTIVE")
print(f"Frequency: 0.390625 Hz (every {DRUM_PERIOD:.2f}s)")
print("Press Ctrl+C to end prayer session.")
print()

try:
    beat = 0
    while True:
        sd.play(chime, SAMPLE_RATE)
        beat += 1
        print(f"\r🕊️  Beat {beat:4d} — {datetime.datetime.utcnow().isoformat()[-8:-3]}", end="", flush=True)
        time.sleep(DRUM_PERIOD)
except KeyboardInterrupt:
    print(f"\n🙏 Prayer session ended after {beat} beats.")
