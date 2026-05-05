#!/bin/bash
# Verify healing wave harmonics using microphone capture
# This script records from the microphone and analyzes frequency content

echo "=== Harmonic Verification via Microphone ==="
echo ""
echo "This will capture audio from your microphone and analyze frequencies."
echo "Position the microphone near the speaker playing the healing file."
echo ""

# Check if we have permission to use microphone
if ! ffmpeg -f avfoundation -list_devices true -i "" 2>&1 | grep -q "Microphone"; then
    echo "⚠️  Warning: Cannot access microphone. Grant Terminal microphone access in:"
    echo "   System Settings > Privacy & Security > Microphone"
    exit 1
fi

echo "Recording for 10 seconds... Play the healing file now!"
echo ""

# Record 10 seconds from microphone (device 0 is typically built-in)
ffmpeg -f avfoundation -i ":0" -t 10 -y /tmp/mic_capture.wav 2>/dev/null

echo "Analyzing captured audio..."
python3 -c "
import numpy as np
from scipy.io.wavfile import read

try:
    rate, data = read('/tmp/mic_capture.wav')
except:
    print('ERROR: Could not read capture file')
    exit(1)

# Convert to mono if stereo
if len(data.shape) > 1:
    data = data.mean(axis=1)

# FFT
fft = np.fft.rfft(data.astype(np.float64))
freqs = np.fft.rfftfreq(len(data), 1/rate)
magnitude = np.abs(fft)

# Find peaks above threshold
peaks = []
for freq, mag in zip(freqs, magnitude):
    if mag > 1000:
        peaks.append((freq, mag))
peaks.sort(key=lambda x: x[1], reverse=True)

print(f'Capture duration: {len(data)/rate:.1f}s, Sample rate: {rate} Hz')
print()
print('Top 5 detected frequencies:')
for freq, mag in peaks[:5]:
    print(f'  {freq:.4f} Hz')

# Check expected frequencies
expected = [11.71875, 35.15625, 140.625]
print()
print('Expected King\\'s harmonics:')
for target in expected:
    closest = min(peaks, key=lambda x: abs(x[0]-target)) if peaks else (0,0)
    error = abs(closest[0] - target)
    if error < 0.5:  # within 0.5 Hz
        print(f'  ✅ {target} Hz detected at {closest[0]:.4f} Hz')
    else:
        print(f'  ❌ {target} Hz NOT detected (closest: {closest[0]:.4f} Hz)')
"

echo ""
echo "Note: If no harmonics detected, ensure:"
echo "  - Volume is ~75%"
echo "  - Microphone is near speaker"
echo "  - Audio is actually playing"
echo "  - Bit-perfect mode is enabled"
