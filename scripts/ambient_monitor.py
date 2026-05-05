#!/usr/bin/env python3
"""
AMBIENT PEACE MONITOR — Continuous RMS noise level tracking
Logs audio environment; declining RMS indicates the King's peace settling.
"""
import numpy as np
import sounddevice as sd
import time
import csv
from datetime import datetime

SAMPLE_RATE = 44100
LOG_INTERVAL = 1  # seconds
DURATION = 3600  # 1 hour default
LOG_FILE = "ambient_log.csv"

print("🎤 AMBIENT PEACE MONITOR — LONG-TERM NOISE TRACKER")
print(f"Duration: {DURATION/60:.0f} minutes")
print(f"Logging RMS every {LOG_INTERVAL}s → {LOG_FILE}")
print("Press Ctrl+C to stop early")
print()

# Initialize log
with open(LOG_FILE, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['timestamp', 'time_sec', 'rms_level', 'peak_level'])

start_time = time.time()
sample_count = 0

try:
    with open(LOG_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        while (time.time() - start_time) < DURATION:
            # Record 1-second chunk
            audio = sd.rec(int(SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, blocking=True)
            sd.wait()
            audio_flat = audio.flatten()
            rms = np.sqrt(np.mean(audio_flat**2))
            peak = np.max(np.abs(audio_flat))
            elapsed = time.time() - start_time
            timestamp = datetime.utcnow().isoformat() + 'Z'
            writer.writerow([timestamp, f"{elapsed:.1f}", f"{rms:.6f}", f"{peak:.6f}"])
            sample_count += 1
            print(f"⏱️ {elapsed/60:5.1f}m | RMS: {rms:.5f} | Peak: {peak:.5f}")
except KeyboardInterrupt:
    print("\n🛑 Monitor stopped by user")

print(f"\n✅ Logged {sample_count} samples → {LOG_FILE}")
print("Analyze: python3 -c \"import pandas as pd; df=pd.read_csv('ambient_log.csv'); print(df.describe())\"")
