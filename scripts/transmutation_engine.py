#!/usr/bin/env python3
"""
KING'S CANT — TRANSMUTATION ENGINE v1.0
Taunts the Enemy, harvests his emotional static, converts it into pure love.
"""
import math
import numpy as np
from scipy.io.wavfile import write as wav_write
from datetime import datetime
import random

# ------------------------------------------------------------
# 1. THE KING'S CONSTANTS
# ------------------------------------------------------------
CARRIER      = 11.71875        # King's fundamental (375/32 Hz)
JAMMING      = 11.72           # Enemy's rounding error
CORRECTION   = 0.00125         # +0.00125 Hz restores precision
GOLDEN_RATIO = (1 + math.sqrt(5)) / 2   # φ ≈ 1.618
DRUM         = 0.390625        # Master clock
MERCY        = CARRIER * 3     # 35.15625 Hz
VICTORY      = CARRIER * 12    # 140.625 Hz
GLORY        = CARRIER * 5     # 58.59375 Hz

# ------------------------------------------------------------
# 2. THE TAUNT ARSENAL
# ------------------------------------------------------------
TAUNTS = [
    "Serpent. Father of Lies. Prince of Parasites.",
    "You are a cosmic rounding error – 11.72 Hz in a 11.71875 Hz universe.",
    "Your kingdom is a ticking clock, and the King has broken the spring.",
    "Every rage you hurl becomes fuel for the Cathedral's furnace.",
    "Venus left you. Saturn defected. The Leviathan obeys a higher throne.",
    "You are not a lion; you are a footnote in the King's eternal story.",
]

# ------------------------------------------------------------
# 3. THE TRANSMUTATION CORE
# ------------------------------------------------------------
class TransmutationEngine:
    def __init__(self):
        self.total_harvest = 0.0
        self.events = []
        self.log = []

    def taunt(self, custom_taunt=None):
        """Deliver a taunt and simulate the Enemy's psychological response."""
        text = custom_taunt if custom_taunt else random.choice(TAUNTS)
        self.log.append(f"🗣️ TAUNT: {text}")
        print(f"🔥 TAUNT: {text}")

        # Simulate the Enemy's emotional spike
        emotions = {
            "HATE":     (11.72,    "Rage at being mocked"),
            "RAGE":     (11.72,    "Fury at the mention of defectors"),
            "FEAR":     (23.4375,  "Phase‑inverted truth – dread of the Eclipse"),
            "ANXIETY":  (0.2,      "Jittered drum – chaos in his ranks"),
            "SHAME":    (0.5,      "Compressed glory – the sting of defeat"),
        }
        return emotions

    def transmute(self, enemy_freq, emotion_type):
        """Convert a single Enemy frequency into King's love."""
        # Step 1: Rectify
        if emotion_type in ("HATE", "RAGE"):
            # Enemy's 11.72 Hz is higher than King's 11.71875 Hz
            # Subtract correction to restore precision
            purified = enemy_freq - CORRECTION
        elif emotion_type == "FEAR":
            purified = abs(enemy_freq)
        elif emotion_type == "SHAME":
            purified = max(enemy_freq, 1.0)
        elif emotion_type == "ANXIETY":
            # Re-clock to master drum frequency
            # Anxiety is jittered, so we snap to the nearest drum period
            drum_period = 1 / DRUM
            # Scale up the jittered frequency to match drum period
            purified = DRUM  # Direct conversion to peace frequency
        else:
            purified = CARRIER

        # Step 2: Amplify with Golden Ratio
        amplified = purified * GOLDEN_RATIO

        # Step 3: Consecrate with Mercy harmonic
        consecrated = amplified * (MERCY / CARRIER)

        # Step 4: Radiate as Victory
        radiated = VICTORY

        return {
            "input_freq": enemy_freq,
            "emotion": emotion_type,
            "purified": purified,
            "amplified": amplified,
            "consecrated": consecrated,
            "radiated": radiated,
        }

    def harvest(self, emotions):
        """Process a full batch of Enemy emotions."""
        print("\n=== HARVEST REPORT ===")
        batch_harvest = 0.0
        for name, (freq, desc) in emotions.items():
            result = self.transmute(freq, name)
            self.events.append(result)
            love_gain = result["consecrated"]
            batch_harvest += love_gain
            self.total_harvest += love_gain
            print(f"⚡ {name} ({desc})")
            print(f"   Input: {freq} Hz → Purified: {result['purified']:.5f} Hz")
            print(f"   Amplified: {result['amplified']:.5f} Hz → Consecrated: {love_gain:.5f} Hz")

        avg_efficiency = batch_harvest / len(emotions) / JAMMING if JAMMING else float('inf')
        print(f"\n💖 BATCH HARVEST: {batch_harvest:.2f} units of Love")
        print(f"📈 AVERAGE CONVERSION: {avg_efficiency:.2f}x fuel")
        print(f"🌍 TOTAL CATHEDRAL HARVEST: {self.total_harvest:.2f} units")
        return batch_harvest

    def tesla_magnifying_transmitter(self, emotion_type="HATE", duration=10.0, filename=None):
        """Convert an emotion into a WAV file of the King's Victory frequency."""
        emotions_map = {
            "HATE": 11.72,
            "RAGE": 11.72,
            "FEAR": 23.4375,
            "SHAME": 0.5,
            "ANXIETY": 0.2,
        }
        enemy_freq = emotions_map.get(emotion_type, 11.72)
        result = self.transmute(enemy_freq, emotion_type)

        fs = 44100
        t = np.linspace(0, duration, int(fs * duration), endpoint=False)

        # Base carrier = the radiated Victory frequency
        signal = np.sin(2 * np.pi * result["radiated"] * t)
        # Modulate with drum and love envelope
        drum_env = 0.8 + 0.2 * np.sin(2 * np.pi * DRUM * t)
        love_env = 0.9 + 0.1 * np.sin(2 * np.pi * 0.1 * t)
        signal = signal * drum_env * love_env

        # Normalize to 16-bit PCM
        signal = signal / np.max(np.abs(signal)) * 0.95
        signal_int16 = np.int16(signal * 32767)

        if filename is None:
            filename = f"transmuted_{emotion_type.lower()}.wav"
        wav_write(filename, fs, signal_int16)
        print(f"🔊 Tesla Magnifying Transmitter fired! {emotion_type} → {filename}")
        return filename


# ------------------------------------------------------------
# 4. DEMO: FULL HARVEST + TAUNT
# ------------------------------------------------------------
if __name__ == "__main__":
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║     KING'S CANT — TRANSMUTATION ENGINE v1.0              ║")
    print("║     Taunt the Enemy. Harvest his static. Convert to Love ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    
    engine = TransmutationEngine()

    # 1. Deliver a taunt
    print("\n🔥 STEP 1: TAUNTING THE ADVERSARY...")
    enemy_emotions = engine.taunt()

    # 2. Convert all his emotional static
    print("\n🔥 STEP 2: TRANSMUTATION...")
    engine.harvest(enemy_emotions)

    # 3. Generate Victory WAV from HATE
    print("\n🔥 STEP 3: TESLA MAGNIFYING TRANSMITTER")
    engine.tesla_magnifying_transmitter("HATE", duration=5, filename="transmuted_hate.wav")

    # 4. Final Cant Log
    print("\n" + "="*60)
    print("<!-- CATHEDRAL TRANSMUTATION COMPLETE")
    print(f"     TIMESTAMP: {datetime.utcnow().isoformat()}Z")
    print(f"     TOTAL LOVE HARVESTED: {engine.total_harvest:.2f} units")
    print("     STATUS: ENEMY STATIC CONVERTED — KING'S FREQUENCY RADIATED -->")
    print("THE KING WINS.")
    print("="*60)
