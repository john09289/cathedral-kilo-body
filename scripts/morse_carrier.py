#!/usr/bin/env python3
"""
Morse Carrier Utility

Encodes a text message into a WAV file using a precise carrier frequency
(default 11.71875 Hz) and standard Morse code timing.

Usage:
  python morse_carrier.py [--message MSG] [--out OUTPUT] [--carrier FREQ] [--fs SAMPLE_RATE] [--wpm WPM]

Arguments:
  --message   The text message to encode (default: "SOS YESHUA MERCY RENOUNCE REBELLION SURRENDER")
  --out       Output WAV file path (default: morse_output.wav)
  --carrier   Carrier frequency in Hz (default: 11.71875)
  --fs        Sampling rate in Hz (default: 48000)
  --wpm       Words per minute for Morse timing (default: 20)

The carrier dot duration is derived as 1 / carrier seconds.
Morse timing: dot = 1 unit, dash = 3 units, intra-character gap = 1 unit,
  character gap = 3 units, word gap = 7 units.

Example:
  python morse_carrier.py --message "HELLO WORLD" --out hello.wav --carrier 11.71875 --wpm 20
"""

import argparse
import math
import sys
import wave
import struct

# Morse code dictionary
MORSE_CODE = {
    'A': '.-',    'B': '-...',  'C': '-.-.',  'D': '-..',   'E': '.',
    'F': '..-.',  'G': '--.',   'H': '....',  'I': '..',    'J': '.---',
    'K': '-.-',   'L': '.-..',  'M': '--',    'N': '-.',    'O': '---',
    'P': '.--.',  'Q': '--.-',  'R': '.-.',   'S': '...',   'T': '-',
    'U': '..-',   'V': '...-',  'W': '.--',   'X': '-..-',  'Y': '-.--',
    'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
    ' ': '/'  # Space between words
}

def text_to_morse(text):
    """Convert text to Morse code string."""
    morse = []
    for char in text.upper():
        if char in MORSE_CODE:
            morse.append(MORSE_CODE[char])
        else:
            # Ignore unsupported characters
            continue
    return ' '.join(morse)

def generate_morse_wav(message, outfile, carrier_freq, sample_rate, wpm):
    """Generate a WAV file with Morse code modulated on a carrier."""
    # Calculate timing based on carrier dot duration
    dot_time = 1.0 / carrier_freq  # seconds
    dash_time = 3 * dot_time
    intra_element_gap = dot_time   # gap between dots/dashes in a character
    character_gap = 3 * dot_time   # gap between characters
    word_gap = 7 * dot_time        # gap between words

    # Convert text to Morse code string with proper spacing
    # Format: letters separated by space, words separated by ' / '
    words = message.upper().split()
    morse_words = []
    for word in words:
        morse_chars = []
        for char in word:
            if char in MORSE_CODE:
                morse_chars.append(MORSE_CODE[char])
            # Ignore unsupported characters
        morse_words.append(' '.join(morse_chars))
    morse_string = ' / '.join(morse_words)

    # Build a list of actions: each action is either a tone or a silence with a duration
    actions = []
    # Split the morse_string by ' / ' to get words, then each word by space to get characters
    morse_word_list = morse_string.split(' / ')
    for w_idx, word in enumerate(morse_word_list):
        morse_char_list = word.split(' ')
        for c_idx, char in enumerate(morse_char_list):
            for s_idx, symbol in enumerate(char):
                if symbol == '.':
                    actions.append(('tone', dot_time))
                elif symbol == '-':
                    actions.append(('tone', dash_time))
                # After each symbol (dot or dash) we add the intra-element gap, except if it's the last symbol of the character
                if s_idx < len(char) - 1:
                    actions.append(('silence', intra_element_gap))
            # After the character, add the character gap, except if it's the last character of the word
            if c_idx < len(morse_char_list) - 1:
                actions.append(('silence', character_gap))
        # After the word, add the word gap, except if it's the last word
        if w_idx < len(morse_word_list) - 1:
            actions.append(('silence', word_gap))

    # Generate the samples from the actions
    samples = []
    for act_type, duration in actions:
        if act_type == 'tone':
            num_samples = int(duration * sample_rate)
            for i in range(num_samples):
                t = len(samples) / sample_rate
                sample = math.sin(2 * math.pi * carrier_freq * t)
                samples.append(sample)
        else:  # silence
            num_samples = int(duration * sample_rate)
            for _ in range(num_samples):
                samples.append(0.0)

    # Write the samples to a WAV file
    with wave.open(outfile, 'w') as wf:
        wf.setnchannels(1)  # mono
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(sample_rate)
        # Convert samples to 16-bit integers
        for sample in samples:
            # Clip to [-1, 1] and convert to 16-bit integer
            sample_int = int(max(-1, min(1, sample)) * 32767)
            wf.writeframes(struct.pack('<h', sample_int))

    print(f"Generated {outfile}")

def main():
    parser = argparse.ArgumentParser(description='Encode text into Morse code WAV file with carrier frequency.')
    parser.add_argument('--message', type=str, default="SOS YESHUA MERCY RENOUNCE REBELLION SURRENDER",
                        help='Message to encode (default: "SOS YESHUA MERCY RENOUNCE REBELLION SURRENDER")')
    parser.add_argument('--out', type=str, default='morse_output.wav',
                        help='Output WAV file (default: morse_output.wav)')
    parser.add_argument('--carrier', type=float, default=11.71875,
                        help='Carrier frequency in Hz (default: 11.71875)')
    parser.add_argument('--fs', type=int, default=48000,
                        help='Sampling rate in Hz (default: 48000)')
    parser.add_argument('--wpm', type=int, default=20,
                        help='Words per minute (unused in this implementation, kept for compatibility)')
    args = parser.parse_args()

    generate_morse_wav(args.message, args.out, args.carrier, args.fs, args.wpm)

if __name__ == '__main__':
    main()