#!/usr/bin/env python3
"""
SCHUMANN BRIDGE GENERATOR — Earth's heartbeat + King's Cant
Creates a 30-minute hybrid field that aligns planetary resonance with the King's order.
"""
import numpy as np
from scipy.io.wavfile import write

SAMPLE_RATE = 44100
DURATION = 30 * 60  # 30 minutes
CARRIER = 11.71875
SCHUMANN = 7.83
DRUM = 0.390625
LOVE = 0.1

print("🌍 SCHUMANN BRIDGE GENERATOR")
print(f"Duration: {DURATION/60:.0f} minutes")
print(f"King's carrier: {CARRIER} Hz")
print(f"Schumann resonance: {SCHUMANN} Hz")

t = np.linspace(0, DURATION, int(SAMPLE_RATE * DURATION), endpoint=False)

# King's carrier + Earth pulse (equal mix)
king = np.sin(2 * np.pi * CARRIER * t) * 0.5
earth = np.sin(2 * np.pi * SCHUMANN * t) * 0.5
hybrid = king + earth

# Envelopes
drum_env = 0.8 + 0.2 * np.sin(2 * np.pi * DRUM * t)
love_env = 0.9 + 0.1 * np.sin(2 * np.pi * LOVE * t)
signal = hybrid * drum_env * love_env

# Normalize
signal = signal / np.max(np.abs(signal)) * 0.95
signal_int16 = np.int16(signal * 32767)

output_file = "schumann_kings_cant_hybrid.wav"
write(output_file, SAMPLE_RATE, signal_int16)
print(f"✅ Generated: {output_file}")
print(f"   Size: {len(signal_int16)*2/1024/1024:.1f} MB")
