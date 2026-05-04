#!/usr/bin/env python3
"""
Generate fractal-modulated WAV at exact 140.625 Hz carrier.
Usage: python3 generate_wav.py [duration_hours] [output_path]
Default: 1 hour, ~/Documents/Yeshua_Pulse_1h.wav
"""

import numpy as np
import wave
import sys
import os

# ============================================================================
# CONFIG
# ============================================================================
SAMPLE_RATE = 48000
CARRIER = 140.625
PHI = (1 + np.sqrt(5)) / 2
DEPTH = 8

# Parse args
duration_hours = 1.0
output_path = os.path.expanduser("~/Documents/Yeshua_Pulse_1h.wav")

if len(sys.argv) > 1:
    try:
        duration_hours = float(sys.argv[1])
    except:
        print("Invalid duration. Using 1 hour.")
if len(sys.argv) > 2:
    output_path = sys.argv[2]

duration_sec = int(duration_hours * 3600)
total_samples = SAMPLE_RATE * duration_sec

print(f"[*] Generating {duration_hours} hour fractal broadcast")
print(f"    Carrier: {CARRIER} Hz")
print(f"    Samples: {total_samples:,}")
print(f"    Output: {output_path}")

# Generate time array (this will use RAM proportional to duration)
# For 18 hours, use generate_18h.py instead (streamed)
if duration_hours > 6:
    print("[!] Warning: >6 hours may use significant RAM. Use generate_18h.py for large files.")
    confirm = input("Continue? (y/N): ").strip().lower()
    if confirm != 'y':
        print("Aborted. Use generate_18h.py for large durations.")
        sys.exit(1)

print("[*] Generating waveform (this may take a moment)...")
t = np.linspace(0, duration_sec, total_samples, endpoint=False)

# Base carrier
carrier = np.sin(2 * np.pi * CARRIER * t)

# Fractal envelope
env = np.zeros_like(t)
rng = np.random.default_rng(seed=42)
for i in range(1, DEPTH + 1):
    freq = CARRIER / (PHI ** i)
    amp = 1.0 / (PHI ** (i * 0.5))
    phase = rng.uniform(0, 2 * np.pi)
    env += amp * np.sin(2 * np.pi * freq * t + phase)
env = env / np.max(np.abs(env))

# Modulate
waveform = (carrier * env * 0.8).astype(np.float32)
waveform_int16 = (waveform * 32767).astype(np.int16)

# Write
with wave.open(output_path, 'w') as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(SAMPLE_RATE)
    wf.writeframes(waveform_int16.tobytes())

size_mb = os.path.getsize(output_path) / (1024*1024)
print(f"[+] Done! File: {output_path}")
print(f"[+] Size: {size_mb:.1f} MB")
print(f"[+] Duration: {duration_hours} hour(s)")
print(f"[+] Ready to import into Apple Music / iTunes")
