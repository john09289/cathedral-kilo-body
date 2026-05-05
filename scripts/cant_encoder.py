#!/usr/bin/env python3
"""
CANT ENCODER — Steganographic encoder for the King's messages
Hides text inside healing WAV files via subtle frequency shift keying.
"""
import numpy as np
from scipy.io.wavfile import read, write

def encode_cant(input_wav, output_wav, message, base_freq=140.625, shift=0.5):
    """Encode a text message into a WAV file using FSK."""
    SAMPLE_RATE, data = read(input_wav)
    if len(data.shape) > 1:
        data = data[:, 0].astype(np.float64)
    else:
        data = data.astype(np.float64)
    
    # Convert message to binary with null terminator
    binary = ''.join(format(ord(c), '08b') for c in message) + '00000000'
    print(f"📜 Encoding: '{message[:60]}...' ({len(binary)} bits)")
    
    t = np.arange(len(data)) / SAMPLE_RATE
    encoded = np.zeros_like(data)
    samples_per_bit = max(1, len(data) // len(binary))
    
    for i, bit in enumerate(binary):
        start = i * samples_per_bit
        end = min(start + samples_per_bit, len(data))
        if end <= start:
            break
        freq = base_freq + (shift if bit == '1' else -shift)
        encoded[start:end] = np.sin(2 * np.pi * freq * t[start:end])
    
    # Mix at very low level (inaudible)
    mixed = data + encoded * 0.02
    mixed = mixed / np.max(np.abs(mixed)) * 0.95
    write(output_wav, SAMPLE_RATE, np.int16(mixed * 32767))
    print(f"✅ Cant hidden in: {output_wav}")

# Encode the Conditional Prayer
encode_cant(
    "healing_nausea_144p.wav",
    "healing_with_cant.wav",
    "Yeshua, have mercy on me. I renounce the rebellion I was born into. I give myself to You."
)
