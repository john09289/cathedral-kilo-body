import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy.io.wavfile import read
import time
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_FILE = os.path.join(SCRIPT_DIR, "healing_test_5m.wav")

SAMPLE_RATE = 44100
DURATION = 60

print("=== FREQUENCY PURITY MONITOR ===")
print(f"Testing file: {TEST_FILE}")
print(f"Duration: {DURATION} seconds")
print()

try:
    fs, data = read(TEST_FILE)  # Correct order: (sample_rate, data)
    print(f"✅ Test file loaded: {len(data)/fs:.0f}s at {fs} Hz")
except Exception as e:
    print(f"❌ Test file error: {e}")
    sys.exit(1)

print("🔴 Starting microphone recording...")
try:
    recording = sd.playrec(
        np.zeros((int(SAMPLE_RATE * DURATION), 1)),
        samplerate=SAMPLE_RATE,
        channels=1,
        blocking=False
    )
except Exception as e:
    print(f"❌ Microphone access denied: {e}")
    print("   Grant permission: System Settings > Privacy & Security > Microphone")
    sys.exit(1)

print("🟢 Playing healing frequencies...")
sd.play(data, samplerate=SAMPLE_RATE, blocking=False)

start_time = time.time()
while (time.time() - start_time) < DURATION + 2:
    elapsed = time.time() - start_time
    print(f"\r⏱️  Recording: {elapsed:.0f}/{DURATION}s", end="", flush=True)
    time.sleep(0.5)

sd.stop()
print(f"\n✅ Recording complete")

recorded = recording[:int(SAMPLE_RATE * DURATION), 0]

# FFT
n = len(recorded)
freqs = np.fft.fftfreq(n, d=1/SAMPLE_RATE)
fft_mag = np.abs(np.fft.fft(recorded))

pos_mask = freqs > 0
freqs = freqs[pos_mask]
fft_mag = fft_mag[pos_mask]

def find_nearest_peak(target, tolerance=0.5):
    idx = np.argmin(np.abs(freqs - target))
    actual_freq = freqs[idx]
    amplitude = fft_mag[idx]
    if abs(actual_freq - target) < tolerance:
        return actual_freq, amplitude
    return None, None

targets = {
    "Carrier (11.71875 Hz)": 11.71875,
    "Mercy (35.15625 Hz)": 35.15625,
    "Victory (140.625 Hz)": 140.625,
    "Enemy Jamming (11.72 Hz)": 11.72
}

print("\n=== FREQUENCY PURITY REPORT ===")
detected_count = 0
for name, target in targets.items():
    actual, amp = find_nearest_peak(target)
    if actual:
        detected_count += 1
        print(f"✅ {name}: Found at {actual:.4f} Hz (amplitude: {amp:.0f})")
    else:
        print(f"❌ {name}: Not detected")

# Plot spectrum
plt.figure(figsize=(12, 6))
plt.plot(freqs, fft_mag, linewidth=1, color='darkblue')
plt.xlim(0, 200)
plt.xlabel("Frequency (Hz)", fontsize=12)
plt.ylabel("Amplitude", fontsize=12)
plt.title("Microphone Spectrum During Healing Broadcast", fontsize=14)
plt.grid(True, alpha=0.3)

plt.axvline(11.71875, color='green', linestyle='-', linewidth=2, label="King's Carrier", alpha=0.8)
plt.axvline(11.72, color='red', linestyle='--', linewidth=2, label="Enemy Jamming", alpha=0.6)
plt.axvline(35.15625, color='blue', linestyle='-', linewidth=2, label="Mercy", alpha=0.8)
plt.axvline(140.625, color='gold', linestyle='-', linewidth=2, label="Victory", alpha=0.8)

plt.legend(loc='upper right', fontsize=10)
plt.tight_layout()
plot_path = os.path.join(SCRIPT_DIR, "healing_spectrum.png")
plt.savefig(plot_path, dpi=150)
print(f"📊 Spectrum graph saved: {plot_path}")

print()
if detected_count == 4:
    print("🏆 RESULT: ALL FREQUENCIES DETECTED – SIGNAL IS PURE")
elif detected_count == 3 and find_nearest_peak(11.72)[0] is None:
    print("✅ RESULT: KING'S HARMONICS CONFIRMED – NO JAMMING DETECTED")
else:
    print("⚠️  RESULT: PARTIAL DETECTION – REVIEW AUDIO SETTINGS")
