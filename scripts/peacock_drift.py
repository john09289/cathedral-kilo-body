import numpy as np
import wave
import struct
import time
from datetime import datetime

# -----------------------------------------------------------
# FRACTAL DRIFT TRANSMITTER — PEACOCK THRONE v50.6
# -----------------------------------------------------------
SAMPLE_RATE = 48000          # Standard audio rate, clean binary multiple
CARRIER = 140.625            # Yeshua Pulse (12th harmonic of 11.71875 Hz)
DURATION = 6 * 60 * 60           # 1 hour broadcast (adjust as needed)
OUTPUT_FILE = "fractal_drift.wav"
LOG_FILE = "cathedral_log.txt"

# Fractal modulation parameters
PHI = (1 + np.sqrt(5)) / 2   # Golden Ratio
DEPTH = 12                   # Recursion depth (higher = finer fractal detail)

# -----------------------------------------------------------
# 1. Generate the fractal envelope (self‑similar amplitude modulation)
# -----------------------------------------------------------
def fractal_envelope(t, depth):
    """Create a recursive, self‑similar modulation envelope."""
    env = np.zeros_like(t)
    for i in range(1, depth + 1):
        freq = CARRIER / (PHI ** i)            # Each layer is a φ‑scaled sub‑harmonic
        amp = 1.0 / (PHI ** (i * 0.5))         # Amplitude decays by φ
        phase = np.random.uniform(0, 2 * np.pi) # Unique phase per layer (creates non‑repeatability)
        env += amp * np.sin(2 * np.pi * freq * t + phase)
    # Normalize to prevent clipping
    env = env / np.max(np.abs(env))
    return env

# -----------------------------------------------------------
# 2. Generate the full fractal‑drift carrier wave
# -----------------------------------------------------------
def generate_fractal_carrier(duration_sec, sample_rate):
    t = np.linspace(0, duration_sec, int(sample_rate * duration_sec), endpoint=False)
    # Base carrier
    base_carrier = np.sin(2 * np.pi * CARRIER * t)
    # Fractal envelope
    env = fractal_envelope(t, DEPTH)
    # Modulate the carrier with the fractal envelope
    waveform = base_carrier * env * 0.8  # 80% amplitude to avoid clipping
    return waveform.astype(np.float32)

# -----------------------------------------------------------
# 3. Write the WAV file
# -----------------------------------------------------------
def write_wav(filename, waveform, sample_rate):
    # Convert to 16‑bit PCM
    waveform_int16 = (waveform * 32767).astype(np.int16)
    with wave.open(filename, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(waveform_int16.tobytes())
    print(f"[+] Fractal drift broadcast saved to {filename}")

# -----------------------------------------------------------
# 4. Persistent time log (memory)
# -----------------------------------------------------------
def log_broadcast():
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    with open(LOG_FILE, 'a') as f:
        f.write(f"{timestamp} | Fractal Drift Broadcast | Carrier: {CARRIER} Hz | Depth: {DEPTH} | Duration: {DURATION}s\n")
    print(f"[+] Logged to {LOG_FILE}")

# -----------------------------------------------------------
# MAIN EXECUTION
# -----------------------------------------------------------
if __name__ == "__main__":
    print(f"[*] Generating fractal drift carrier at {CARRIER} Hz...")
    waveform = generate_fractal_carrier(DURATION, SAMPLE_RATE)
    write_wav(OUTPUT_FILE, waveform, SAMPLE_RATE)
    log_broadcast()
    print("[*] Broadcast complete. The Peacock Throne sings.")
