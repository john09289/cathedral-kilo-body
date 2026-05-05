#!/usr/bin/env python3
"""
STARLINK CANT RELAY — Encodes the Conditional Prayer into RF-ready IQ data
Simulates a satellite uplink with the King's frequencies.
"""
import numpy as np

SAMPLE_RATE = 2000000  # 2 MSPS (typical SDR rate)
DURATION = 10.0
CARRIER = 11.71875
MESSAGE = "YESHUA_MERCY_SURRENDER"

def text_to_morse(text):
    code = {
        'Y': '-.--', 'E': '.', 'S': '...', 'H': '....', 'U': '..-',
        'A': '.-', 'M': '--', 'C': '-.-.', 'R': '.-.', 'N': '-.',
        'D': '-..', '_': '/', ' ': ' '
    }
    return ' '.join(code.get(c, '?') for c in text.upper())

morse = text_to_morse(MESSAGE)
print("🛰️ STARLINK CANT RELAY")
print(f"Message: {MESSAGE}")
print(f"Morse: {morse}")

t = np.linspace(0, DURATION, int(SAMPLE_RATE * DURATION), endpoint=False)
carrier_i = np.cos(2 * np.pi * CARRIER * t)
carrier_q = np.sin(2 * np.pi * CARRIER * t)

# On-off keying modulation
dot_len = int(SAMPLE_RATE * 0.1)  # 100 ms dot
signal = np.zeros(len(t))
pos = 0
for symbol in morse:
    if symbol == '.':
        if pos + dot_len <= len(signal):
            signal[pos:pos+dot_len] = 1.0
        pos += dot_len + dot_len  # dot + intra-char space
    elif symbol == '-':
        if pos + 3*dot_len <= len(signal):
            signal[pos:pos+3*dot_len] = 1.0
        pos += 3*dot_len + dot_len
    elif symbol == '/':
        pos += 7*dot_len  # word space
    else:
        pos += dot_len

# IQ modulation (complex baseband)
iq_data = np.empty(len(t)*2, dtype=np.float32)
iq_data[0::2] = carrier_i * signal * 0.5
iq_data[1::2] = carrier_q * signal * 0.5

output_file = "starlink_relay.iq"
iq_data.tofile(output_file)
print(f"✅ RF-ready IQ file: {output_file}")
print(f"   Samples: {len(iq_data)//2} ({len(iq_data)} floats)")
print(f"   Duration: {DURATION}s @ {SAMPLE_RATE/1e6:.1f} MSPS")
