#!/usr/bin/env python3
"""
GENERATE 18-HOUR FRACTAL DRIFT — Pure WAV
Streams to disk in chunks to avoid memory overflow.
Output: Yeshua_Pulse_18h.wav (pure, uncompressed, 18 hours)
"""

import numpy as np
import wave
import sys
import time

# ============================================================================
# CONFIG
# ============================================================================
SAMPLE_RATE = 48000
CARRIER = 140.625
PHI = (1 + np.sqrt(5)) / 2
DEPTH = 8
DURATION_HOURS = 18
OUTPUT_FILE = f"/Users/nicholashughes/Documents/Yeshua_Pulse_{DURATION_HOURS}h.wav"

# Chunk size: 1 minute at a time (to stay under RAM limits)
CHUNK_SECONDS = 60
SAMPLES_PER_CHUNK = SAMPLE_RATE * CHUNK_SECONDS
TOTAL_CHUNKS = (DURATION_HOURS * 3600) // CHUNK_SECONDS

print(f"[*] Generating {DURATION_HOURS}-hour fractal broadcast (streamed to disk)")
print(f"    Carrier: {CARRIER} Hz")
print(f"    Sample rate: {SAMPLE_RATE} Hz")
print(f"    Chunk size: {CHUNK_SECONDS}s")
print(f"    Total chunks: {TOTAL_CHUNKS}")
print(f"    Output: {OUTPUT_FILE}")
print()

# Precompute LFO parameters (fixed across all chunks)
rng = np.random.default_rng(seed=42)  # Fixed seed for reproducibility
lfo_params = []
for i in range(1, DEPTH + 1):
    freq = CARRIER / (PHI ** i)
    amp = 1.0 / (PHI ** (i * 0.5))
    phase = rng.uniform(0, 2 * np.pi)
    lfo_params.append((freq, amp, phase))

# Open WAV file for writing
with wave.open(OUTPUT_FILE, 'w') as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)  # 16-bit
    wf.setframerate(SAMPLE_RATE)

    total_samples_written = 0
    start_time = time.time()

    for chunk_idx in range(TOTAL_CHUNKS):
        # Time array for this chunk
        t0 = chunk_idx * CHUNK_SECONDS
        t = np.linspace(t0, t0 + CHUNK_SECONDS, SAMPLES_PER_CHUNK, endpoint=False)

        # Base carrier
        carrier_wave = np.sin(2 * np.pi * CARRIER * t)

        # Fractal envelope (sum of φ-scaled LFOs)
        env = np.zeros_like(t)
        for freq, amp, phase in lfo_params:
            env += amp * np.sin(2 * np.pi * freq * t + phase)
        env = env / np.max(np.abs(env))

        # Modulate and scale
        waveform = (carrier_wave * env * 0.8).astype(np.float32)
        waveform_int16 = (waveform * 32767).astype(np.int16)

        # Write chunk
        wf.writeframes(waveform_int16.tobytes())
        total_samples_written += len(waveform_int16)

        # Progress
        elapsed = time.time() - start_time
        progress = (chunk_idx + 1) / TOTAL_CHUNKS * 100
        print(f"\r[{chunk_idx+1:4d}/{TOTAL_CHUNKS}] {progress:.1f}% | "
              f"Written: {total_samples_written/SAMPLE_RATE/3600:.2f} hr | "
              f"Elapsed: {elapsed/60:.1f} min", end="", flush=True)

    print("\n[+] Write complete.")

# Final stats
file_size_mb = total_samples_written * 2 / (1024 * 1024)  # 16-bit = 2 bytes per sample
print(f"[+] File size: {file_size_mb:.1f} MB")
print(f"[+] Duration: {total_samples_written/SAMPLE_RATE/3600:.2f} hours")
print(f"[+] Ready for Apple Music / iTunes import")
