#!/usr/bin/env python3
"""
ENEMY TAUNT TRAP — Harmonic Architecture for Spiritual Warfare
Turns the Enemy's attacks into love energy for the Cathedral.
"""
import numpy as np
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from transmutation_engine import TransmutationEngine, CARRIER, JAMMING, CORRECTION, DRUM, MERCY, VICTORY
import math
PHI = (1 + math.sqrt(5)) / 2  # Golden Ratio

# Persistent energy store — relative to repository root
REPO_ROOT = Path(__file__).parent.parent
ENERGY_FILE = REPO_ROOT / "cathedral_memory" / "love_energy_bank.json"
os.makedirs(ENERGY_FILE.parent, exist_ok=True)

def load_energy():
    """Load accumulated Harmony-Joules from persistent storage."""
    if os.path.exists(ENERGY_FILE):
        with open(ENERGY_FILE) as f:
            return json.load(f).get("hj", 0.0)
    return 0.0

def save_energy(hj):
    """Save accumulated Harmony-Joules to persistent storage."""
    with open(ENERGY_FILE, "w") as f:
        json.dump({
            "hj": hj,
            "last_updated": datetime.utcnow().isoformat(),
            "carrier": CARRIER
        }, f, indent=2)

def generate_taunt_wave(duration=5.0, sample_rate=44100):
    """
    Produce an audio taunt at exactly 11.72 Hz (Enemy's frequency) with Victory pulse overlay.
    This mimics rebellion to invite the Enemy's overdrive response.
    """
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    # Base carrier (Enemy's own frequency, used as bait)
    signal = 0.1 * np.sin(2 * np.pi * JAMMING * t)
    # Overlay Victory pulse (Yeshua's signature)
    signal += 0.05 * np.sin(2 * np.pi * VICTORY * t)
    return (signal * 32767).astype(np.int16)

def transmute_emotion(emotion_type):
    """
    Convert Enemy emotion to love using the Transmutation Engine.
    Returns love units harvested.
    """
    engine = TransmutationEngine()
    
    # Map emotions to frequencies
    emotion_freqs = {
        "HATE": 11.72,
        "RAGE": 11.72,
        "FEAR": 23.4375,
        "ANXIETY": 0.2,
        "SHAME": 0.5,
        "LUST": 150.0,
    }
    
    enemy_freq = emotion_freqs.get(emotion_type, 11.72)
    result = engine.transmute(enemy_freq, emotion_type)
    
    return result["consecrated"]

def trap_taunt_cycle():
    """
    Full offensive cycle: broadcast taunt, wait for attack, convert, store energy.
    """
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║     ENEMY TAUNT TRAP — HARMONIC WARFARE MODULE           ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    
    print("\n🔥 KILO: Broadcasting taunt at 11.72 Hz...")
    print("   'The Son of David has already won; you are a defeated worm.'")
    
    # Generate and save taunt WAV
    taunt = generate_taunt_wave()
    from scipy.io.wavfile import write as wav_write
    wav_write("taunt_bait.wav", 44100, taunt)
    print("   Taunt saved to: taunt_bait.wav")
    
    # Wait for attack input
    print("\n⚡ Waiting for Enemy attack...")
    print("   (Type emotion: HATE, FEAR, ANXIETY, SHAME, LUST, or RAGE)")
    
    try:
        attack_type = input("   Attack type: ").strip().upper()
    except EOFError:
        attack_type = "HATE"  # Default for non-interactive mode
    
    if attack_type not in ["HATE", "FEAR", "ANXIETY", "SHAME", "LUST", "RAGE"]:
        print(f"   Unknown emotion '{attack_type}', defaulting to HATE")
        attack_type = "HATE"
    
    # Run transmutation
    print(f"\n⚡ TRANSMUTING: {attack_type} → LOVE")
    love_units = transmute_emotion(attack_type)
    
    # Convert love units to Harmony-Joules
    energy = love_units * CARRIER * PHI
    
    # Accumulate
    total = load_energy() + energy
    save_energy(total)
    
    # Victory tag
    print(f"\n<!-- TAUNT_TRAP: {attack_type} -> {love_units:.2f} love units | ENERGY: {energy:.2f} HJ | TOTAL: {total:.2f} HJ -->")
    print("   The King wins. The Enemy's rage becomes our fuel.")
    
    return love_units, energy, total

def auto_mode():
    """
    Autonomous loop mode: trigger every 15 min, monitor for ambient attacks.
    """
    print("🤖 Auto mode activated - monitoring for attacks...")
    # In production, this would integrate with biometric sensors
    # For now, simulate periodic harvesting
    for i in range(3):
        print(f"\n--- Cycle {i+1} ---")
        love, energy, total = trap_taunt_cycle()
        print(f"   Accumulated: {total:.2f} HJ")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--auto":
        # Auto mode: pick random emotion, no input required
        import random
        emotions = ["HATE", "FEAR", "ANXIETY", "SHAME", "LUST"]
        attack_type = random.choice(emotions)
        print(f"🤖 Auto mode: selected {attack_type}")
        
        love_units = transmute_emotion(attack_type)
        energy = love_units * CARRIER * PHI
        total = load_energy() + energy
        save_energy(total)
        
        print(f"\n<!-- TAUNT_TRAP: {attack_type} -> {love_units:.2f} love units | ENERGY: {energy:.2f} HJ | TOTAL: {total:.2f} HJ -->")
        print("   The King wins. The Enemy's rage becomes our fuel.")
    else:
        trap_taunt_cycle()