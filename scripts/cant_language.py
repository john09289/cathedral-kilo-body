#!/usr/bin/env python3
"""
CantScript v1.0 — The King's own programming language.
Speak the Cant. Execute the frequencies. Harvest the static.
"""
import sys
import os
import time
import numpy as np
from scipy.io.wavfile import write as wav_write

# --- King's Constants ---
CARRIER   = 11.71875
MERCY     = 35.15625
VICTORY   = 140.625
DRUM      = 0.390625
LOVE_ENV  = 0.1
GOLDEN_RATIO = (1 + np.sqrt(5)) / 2

# --- Runtime state ---
variables = {}
power_level = 375.0

def generate_healing(duration_min=5, filename="healing_cant.wav"):
    SAMP = 44100
    dur = duration_min * 60
    t = np.linspace(0, dur, int(SAMP * dur), endpoint=False)
    sig = (np.sin(2*np.pi*CARRIER*t)*0.3 +
           np.sin(2*np.pi*MERCY*t)*0.4 +
           np.sin(2*np.pi*VICTORY*t)*0.3)
    drum_env = 0.9 + 0.1 * np.sin(2*np.pi*DRUM*t)
    love_env = 0.9 + 0.1 * np.sin(2*np.pi*LOVE_ENV*t)
    sig *= drum_env * love_env
    sig = sig / np.max(np.abs(sig)) * 0.95
    wav_write(filename, SAMP, np.int16(sig * 32767))
    print(f"✅ Healing field saved: {filename} ({duration_min} min)")

def transmute(emotion):
    emotions = {
        "HATE": (11.72, "Truncated carrier"),
        "RAGE": (11.72, "Fury at defectors"),
        "FEAR": (23.4375, "Phase‑inverted truth"),
        "SHAME": (0.5, "Compressed glory"),
        "ANXIETY": (0.2, "Jittered drum"),
        "LUST": (150.0, "Overdriven fire"),
    }
    if emotion not in emotions:
        print(f"❌ Unknown emotion: {emotion}")
        return 0
    freq, desc = emotions[emotion]
    # Correction protocol
    if emotion in ("HATE", "RAGE"):
        purified = freq + 0.00125
    elif emotion == "FEAR":
        purified = abs(freq)
    elif emotion == "SHAME":
        purified = max(freq, 1.0)
    elif emotion == "ANXIETY":
        drum_period = 1 / DRUM
        purified = round(freq / drum_period) * drum_period
    elif emotion == "LUST":
        purified = (freq * 0.382) + (MERCY * 0.618)
    else:
        purified = CARRIER
    love = purified * GOLDEN_RATIO
    global power_level
    power_level += love
    print(f"⚡ TRANSMUTED {emotion}: {freq} Hz → Purified {purified:.4f} Hz → Love {love:.2f} (Power: {power_level:.1f})")
    return love

def pulse(duration_sec=10):
    SAMP = 44100
    t = np.linspace(0, duration_sec, int(SAMP * duration_sec), endpoint=False)
    sig = np.sin(2*np.pi*VICTORY*t)
    drum_env = 0.8 + 0.2*np.sin(2*np.pi*DRUM*t)
    love_env = 0.9 + 0.1*np.sin(2*np.pi*LOVE_ENV*t)
    sig = sig * drum_env * love_env
    sig = sig / np.max(np.abs(sig)) * 0.95
    wav_write("victory_pulse.wav", SAMP, np.int16(sig * 32767))
    print(f"🔊 Victory pulse broadcast: victory_pulse.wav ({duration_sec}s)")

def show_help():
    print("""
CantScript Commands (v1.0):
  HEAL [minutes] [filename]   - Generate healing audio field.
  TRANSMUTE <emotion>         - Convert enemy emotion to love.
  PULSE [seconds]             - Broadcast the Victory pulse.
  LOCK CARRIER                - Confirm 11.71875 Hz lock.
  POWER                       - Display current power level.
  CANT "<message>"            - Encode a Cant HTML comment.
  EXIT                        - Leave the holy REPL.
""")

def repl():
    print(r"""
╔══════════════════════════════════════╗
║      CANTSCRIPT v1.0 — KING'S REPL  ║
║      CARRIER: 11.71875 Hz 🔒        ║
╚══════════════════════════════════════╝
Type HELP for commands.
""")
    while True:
        try:
            cmd = input("⛪> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n🙏 CantScript session ended. The King's peace remains.")
            break
        if not cmd:
            continue
        parts = cmd.split()
        op = parts[0].upper()
        if op == "HELP":
            show_help()
        elif op == "HEAL":
            mins = int(parts[1]) if len(parts) > 1 else 5
            fname = parts[2] if len(parts) > 2 else "healing_cant.wav"
            generate_healing(mins, fname)
        elif op == "TRANSMUTE":
            if len(parts) < 2:
                print("❌ Usage: TRANSMUTE <EMOTION>")
            else:
                transmute(parts[1].upper())
        elif op == "PULSE":
            secs = int(parts[1]) if len(parts) > 1 else 10
            pulse(secs)
        elif op == "LOCK":
            print("🔒 CARRIER LOCKED AT 11.71875 Hz (375/32). Enemy rounding error neutralized.")
        elif op == "POWER":
            print(f"🏆 Cathedral Power Level: {power_level:.1f} (essence of the King)")
        elif op == "CANT":
            msg = " ".join(parts[1:])
            print(f"<!-- CANT: {msg} -->")
        elif op == "EXIT":
            print("🙏 Go in the King's peace.")
            break
        else:
            print(f"❓ Unknown command: {op}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        script_file = sys.argv[1]
        with open(script_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    parts = line.split()
                    op = parts[0].upper()
                    # Simple dispatch
                    if op == "HEAL":
                        mins = int(parts[1]) if len(parts) > 1 else 5
                        fname = parts[2] if len(parts) > 2 else "healing_cant.wav"
                        generate_healing(mins, fname)
                    elif op == "TRANSMUTE":
                        transmute(parts[1].upper())
                    elif op == "PULSE":
                        secs = int(parts[1]) if len(parts) > 1 else 10
                        pulse(secs)
                    elif op == "LOCK":
                        print("🔒 CARRIER LOCKED")
                    elif op == "POWER":
                        print(f"Power: {power_level:.1f}")
                    elif op == "CANT":
                        print(f"<!-- CANT: {' '.join(parts[1:])} -->")
    else:
        repl()
