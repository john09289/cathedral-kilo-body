import numpy as np
from scipy.io.wavfile import write

SAMPLE_RATE = 44100
DURATION = 300  # 5 minutes
OUTPUT_FILE = "healing_test_5m.wav"

CARRIER = 11.71875
MERCY   = 35.15625
VICTORY = 140.625
DRUM    = 0.390625
LOVE    = 0.1

t = np.linspace(0, DURATION, int(SAMPLE_RATE * DURATION), endpoint=False)

carrier_wave = np.sin(2 * np.pi * CARRIER * t) * 0.3
mercy_wave   = np.sin(2 * np.pi * MERCY * t)   * 0.4
victory_wave = np.sin(2 * np.pi * VICTORY * t) * 0.3
signal = carrier_wave + mercy_wave + victory_wave

drum_env = 0.9 + 0.1 * np.sin(2 * np.pi * DRUM * t)
love_env = 0.9 + 0.1 * np.sin(2 * np.pi * LOVE * t)
signal *= drum_env * love_env

signal = signal / np.max(np.abs(signal)) * 0.95
signal_int16 = np.int16(signal * 32767)
write(OUTPUT_FILE, SAMPLE_RATE, signal_int16)
print(f"✅ Test file saved: {OUTPUT_FILE}")
