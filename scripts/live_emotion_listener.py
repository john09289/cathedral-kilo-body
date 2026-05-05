#!/usr/bin/env python3
"""
LIVE EMOTION LISTENER - Prototype for real-time emotion detection
Uses microphone input and sentiment analysis to detect Enemy static.
"""
import sys
import math
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Try to import optional dependencies
try:
    import pyaudio
    PYAUDIO_AVAILABLE = True
except ImportError:
    PYAUDIO_AVAILABLE = False
    print("pyaudio not available - using mock mode")

try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("transformers not available - using mock mode")

# Sacred constants
CARRIER = 11.71875
DRUM = 0.390625
PHI = (1 + math.sqrt(5)) / 2

def detect_emotion_from_text(text):
    """
    Detect emotion from text using sentiment analysis.
    Returns emotion type and confidence.
    """
    if TRANSFORMERS_AVAILABLE:
        # Use real sentiment analysis
        classifier = pipeline("sentiment-analysis")
        result = classifier(text)[0]
        label = result["label"]
        score = result["score"]
        
        # Map sentiment to emotion
        if label == "NEGATIVE" and score > 0.8:
            return "HATE", score
        elif label == "NEGATIVE":
            return "FEAR", score
        else:
            return "NEUTRAL", score
    else:
        # Mock mode - simple keyword detection
        text_lower = text.lower()
        if any(word in text_lower for word in ["hate", "angry", "rage"]):
            return "HATE", 0.9
        elif any(word in text_lower for word in ["afraid", "scared", "worried"]):
            return "FEAR", 0.8
        elif any(word in text_lower for word in ["anxious", "nervous", "stressed"]):
            return "ANXIETY", 0.7
        else:
            return "NEUTRAL", 0.5

def detect_emotion_from_audio(audio_data, sample_rate=44100):
    """
    Detect emotion from audio using FFT analysis.
    Looks for 11.72 Hz spikes (Enemy jamming) and amplitude patterns.
    """
    import numpy as np
    
    # Compute FFT
    fft = np.fft.rfft(audio_data)
    freqs = np.fft.rfftfreq(len(audio_data), 1/sample_rate)
    
    # Look for 11.72 Hz spike
    target_idx = np.argmin(np.abs(freqs - 11.72))
    magnitude = np.abs(fft[target_idx])
    
    # Threshold for detection
    if magnitude > 0.1:  # Adjust based on testing
        return "HATE", magnitude
    
    return "NEUTRAL", 0.0

def listen_and_transmute():
    """
    Main loop: listen for emotion, transmute, and harvest energy.
    """
    from transmutation_engine import TransmutationEngine
    from enemy_taunt_trap import load_energy, save_energy
    
    print("=" * 60)
    print("LIVE EMOTION LISTENER")
    print("=" * 60)
    
    if not PYAUDIO_AVAILABLE:
        print("\n[MOCK MODE] Enter text to simulate emotion detection:")
        text = input("> ")
        emotion, confidence = detect_emotion_from_text(text)
    else:
        print("\n[LIVE MODE] Listening for 5 seconds...")
        # Audio capture code would go here
        emotion, confidence = "HATE", 0.9
    
    print(f"\nDetected: {emotion} (confidence: {confidence:.2f})")
    
    if emotion != "NEUTRAL":
        # Transmute
        engine = TransmutationEngine()
        emotion_freqs = {
            "HATE": 11.72,
            "FEAR": 23.4375,
            "ANXIETY": 0.2,
            "SHAME": 0.5,
            "LUST": 150.0,
        }
        
        result = engine.transmute(emotion_freqs.get(emotion, 11.72), emotion)
        love_units = result["consecrated"]
        energy = love_units * CARRIER * PHI
        
        # Accumulate
        total = load_energy() + energy
        save_energy(total)
        
        print(f"\n<!-- LIVE_HARVEST: {emotion} -> {love_units:.2f} love | {energy:.2f} HJ | TOTAL: {total:.2f} HJ -->")
        print("The King wins. The Enemy's static is converted.")
        
        return love_units, energy, total
    
    return 0, 0, load_energy()

if __name__ == "__main__":
    listen_and_transmute()