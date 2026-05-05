import numpy as np
from scipy.io.wavfile import write

# -----------------------------------------------------------
# THE HEALING WAVE – Nausea Relief (King's Cant)
# -----------------------------------------------------------
SAMPLE_RATE = 44100          # Standard CD quality
DURATION = 300               # 5 minutes
OUTPUT_FILE = "healing_nausea_144p.wav"

# King's precise frequencies
CARRIER = 11.71875           # Earth fundamental
MERCY   = 35.15625           # 3:1 – Covenant / Mercy
VICTORY = 140.625            # 12:1 – Yeshua Pulse
DRUM    = 0.390625           # Master Clock
LOVE    = 0.1                # Slow breathing envelope

t = np.linspace(0, DURATION, int(SAMPLE_RATE * DURATION), endpoint=False)

# Base carrier – silent, inaudible, but creates the healing field
carrier_wave = np.sin(2 * np.pi * CARRIER * t)

# Mercy harmonic – resonates with the stomach and vagus nerve
mercy_wave = np.sin(2 * np.pi * MERCY * t)

# Victory pulse – shatters the Enemy's 11.72 Hz nausea signal
victory_wave = np.sin(2 * np.pi * VICTORY * t)

# Drum – gentle rhythmic grounding every ~2.56 seconds
drum_env = 0.9 + 0.1 * np.sin(2 * np.pi * DRUM * t)

# Love envelope – slow, soothing rise and fall
love_env = 0.9 + 0.1 * np.sin(2 * np.pi * LOVE * t)

# Combine with equal weighting, then apply dynamic envelopes
signal = (carrier_wave * 0.3 + mercy_wave * 0.4 + victory_wave * 0.3)
signal = signal * drum_env * love_env

# Smooth fade-in and fade-out (5 seconds each)
fade_samples = SAMPLE_RATE * 5
fade_in = np.linspace(0, 1, fade_samples)
fade_out = np.linspace(1, 0, fade_samples)
signal[:fade_samples] *= fade_in
signal[-fade_samples:] *= fade_out

# Normalize to 16-bit PCM range
signal = signal / np.max(np.abs(signal)) * 0.95  # leave a little headroom
signal_int16 = np.int16(signal * 32767)

write(OUTPUT_FILE, SAMPLE_RATE, signal_int16)
print(f"✅ Healing wave saved to {OUTPUT_FILE}")
print(f"   Frequencies: {CARRIER} Hz carrier + {MERCY} Hz mercy + {VICTORY} Hz victory")
print(f"   Drum: {DRUM} Hz   Love breath: {LOVE} Hz")
print(f"   Duration: {DURATION} seconds")
print(f"   Ready for Apple Music / desktop playback.")
