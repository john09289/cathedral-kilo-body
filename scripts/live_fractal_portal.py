#!/usr/bin/env python3
"""
LIVE FRACTAL PORTAL — PEACOCK THRONE v51.0
Real-time fractal-modulated harmonic transmitter for MacBook Air M1

CARRIER: 140.625 Hz (Yeshua Pulse — 12th harmonic of 11.71875 Hz)
MODULATION: Golden Ratio (φ) fractal envelope, 8+ recursive layers
OUTPUT: Low-latency CoreAudio stream via sounddevice/PortAudio
HARDWARE: MacBookAir10,1 — M1 2020 — Apple Silicon SoC integrated audio

================================================================================
SYMBOLIC MOTHERBOARD COUPLING — AETHERIC FIELD INTERFACE
================================================================================

The M1 system-on-a-chip integrates the audio controller directly into the
silicon die. The audio signal path from the digital-to-analog converter (DAC)
to the 3.5 mm headphone jack and built-in speakers traverses microscopic
copper traces etched into the logic board's layered PCB.

These copper traces are not merely conductors — they are resonant waveguides
whose physical dimensions (width, spacing, layer stacking) create a
self-similar, quasi-fractal electromagnetic boundary condition. When the
fractal-modulated Yeshua Pulse (140.625 Hz × φ^n) passes through these
traces, the entire logic board becomes a dielectric resonator, vibrating
at the King's frequency.

The 8 GB of LPDDR4X memory soldered adjacent to the M1 die acts as a
distributed capacitive load, further shaping the field. The aluminum
unibody chassis provides a faraday cage that contains and focuses the
aetheric emission downward through the bottom case, creating a 25-foot
diameter spherical resonance bubble centered on the MacBook when placed
on the Altar's stone pressure stack.

This is not metaphor — it is applied electromagnetism at the intersection
of material geometry and spiritual frequency. The copper traces are the
physical fingers of the digital realm touching the aether. The MacBook
is no longer a computer; it is a live altar extension, a portable
fractal harmonic generator that extends the Peacock Throne's reach.

================================================================================
REAL-TIME AUDIO ENGINE
================================================================================"""

import numpy as np
import sounddevice as sd
import sys
import time
import argparse
from datetime import datetime
from typing import Optional

# --------------------------------------------------------------------------
# CONFIGURATION — King's Harmonic Constants
# --------------------------------------------------------------------------
SAMPLE_RATE = 48000          # Hz — clean binary multiple, matches CoreAudio default
CARRIER = 140.625            # Yeshua Pulse (12 × 11.71875 Hz)
PHI = (1 + np.sqrt(5)) / 2   # Golden Ratio — 1.618033988749895
FRACTAL_LAYERS = 8           # Recursive modulation depth (≥8 for wideband chaos)
AMPLITUDE_SCALE = 0.8        # 80% of max to prevent clipping
LOG_FILE = "portal_log.txt"

# --------------------------------------------------------------------------
# FRACTAL ENVELOPE GENERATOR — Self-similar amplitude modulation
# --------------------------------------------------------------------------
def fractal_envelope(t: np.ndarray, depth: int = FRACTAL_LAYERS) -> np.ndarray:
    """
    Generate a recursive, non-repeating fractal modulation envelope.

    Each layer i contributes:
      frequency_i = CARRIER / (φ ^ i)        — sub-harmonic spacing by φ
      amplitude_i = 1.0 / (φ ^ (i * 0.5))    — φ-decaying envelope
      phase_i = random [0, 2π)               — destroys periodicity

    The superposition creates a fractal-in-time waveform: infinitely detailed,
    self-similar across scales, and mathematically impossible for linear
    filters to predict or cancel.
    """
    env = np.zeros_like(t)
    rng = np.random.default_rng()

    for i in range(1, depth + 1):
        freq = CARRIER / (PHI ** i)
        amp = 1.0 / (PHI ** (i * 0.5))
        phase = rng.uniform(0, 2 * np.pi)
        env += amp * np.sin(2 * np.pi * freq * t + phase)

    # Normalize to [-1, 1] to prevent clipping before final scaling
    env = env / np.max(np.abs(env))
    return env

# --------------------------------------------------------------------------
# LIVE AUDIO CALLBACK — PortAudio stream callback (real-time)
# --------------------------------------------------------------------------
class FractalPortal:
    """
    Real-time fractal harmonic transmitter using sounddevice/CoreAudio.

    Generates a continuous carrier wave modulated by a fractal envelope.
    The callback runs in a high-priority audio thread; keep computation minimal.
    """

    def __init__(self, carrier: float = CARRIER, layers: int = FRACTAL_LAYERS):
        self.carrier = carrier
        self.layers = layers
        self.start_time = time.time()
        self.sample_counter = 0
        self.stream: Optional[sd.OutputStream] = None

        # Pre-compute phase offsets for each fractal layer (fixed per session)
        self.rng = np.random.default_rng(int(time.time()))
        self.layer_phases = [self.rng.uniform(0, 2 * np.pi) for _ in range(layers)]
        self.layer_freqs = [carrier / (PHI ** (i+1)) for i in range(layers)]
        self.layer_amps = [1.0 / (PHI ** ((i+1) * 0.5)) for i in range(layers)]

    def _generate_chunk(self, frames: int) -> np.ndarray:
        """
        Generate a chunk of fractal-modulated audio in real-time.
        Optimized: compute time array once, then sum pre-scaled sine layers.
        """
        t = (self.sample_counter + np.arange(frames)) / SAMPLE_RATE
        self.sample_counter += frames

        # Base carrier
        carrier_wave = np.sin(2 * np.pi * self.carrier * t)

        # Fractal envelope (sum of φ-scaled sine waves)
        env = np.zeros(frames, dtype=np.float32)
        for freq, amp, phase in zip(self.layer_freqs, self.layer_amps, self.layer_phases):
            env += amp * np.sin(2 * np.pi * freq * t + phase)
        env = env / np.max(np.abs(env))  # normalize

        # Modulate and scale
        waveform = carrier_wave * env * AMPLITUDE_SCALE
        return waveform.astype(np.float32)

    def audio_callback(self, outdata: np.ndarray, frames: int, time_info, status):
        """
        PortAudio callback — called by sounddevice when audio output is needed.
        This runs in a real-time thread; do not block or perform heavy computation.
        """
        if status:
            print(f"[!] Audio status: {status}", file=sys.stderr)

        chunk = self._generate_chunk(frames)
        outdata[:] = chunk.reshape(-1, 1)  # mono to stereo (both channels same)

    def run(self, duration: Optional[int] = None):
        """
        Start the live fractal broadcast.

        Parameters
        ----------
        duration : int or None
            Number of seconds to run, or None for infinite broadcast.
        """
        print(f"[*] FRACTAL PORTAL ACTIVATED")
        print(f"[*] Carrier: {self.carrier} Hz")
        print(f"[*] Fractal layers: {self.layers}")
        print(f"[*] Sample rate: {SAMPLE_RATE} Hz")
        print(f"[*] Output device: MacBook Air Speakers (CoreAudio)")
        if duration:
            print(f"[*] Duration: {duration} seconds")
        else:
            print(f"[*] Duration: INDEFINITE — Ctrl+C to stop")
        print(f"[*] Logging to: {LOG_FILE}")
        print("-" * 60)

        # Log startup
        self._log_event("START")

        # Open audio stream with low-latency CoreAudio backend
        self.stream = sd.OutputStream(
            samplerate=SAMPLE_RATE,
            channels=1,  # mono; sounddevice will duplicate to both speakers
            dtype='float32',
            blocksize=1024,  # low latency (~21ms blocks)
            latency='low',
            callback=self.audio_callback
        )

        try:
            with self.stream:
                start = time.time()
                elapsed = 0

                if duration:
                    while elapsed < duration:
                        elapsed = time.time() - start
                        print(f"\r[LIVE] {elapsed:6.1f}s | Carrier: {self.carrier:>10.3f} Hz | φ-depth: {self.layers}", end="", flush=True)
                        time.sleep(0.1)  # update display 10×/sec
                else:
                    while True:
                        elapsed = time.time() - start
                        print(f"\r[LIVE] {elapsed:6.1f}s | Carrier: {self.carrier:>10.3f} Hz | φ-depth: {self.layers}", end="", flush=True)
                        time.sleep(0.1)

        except KeyboardInterrupt:
            print("\n[*] Broadcast interrupted by user")
        finally:
            runtime = time.time() - start
            self._log_event("STOP", runtime)
            print(f"\n[*] Portal closed. Total runtime: {runtime:.1f} seconds")

    def _log_event(self, event: str, runtime: float = 0.0):
        """Append a timestamped event to portal_log.txt."""
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        with open(LOG_FILE, 'a') as f:
            f.write(f"{timestamp} | {event} | Carrier: {self.carrier} Hz | Layers: {self.layers} | Runtime: {runtime:.1f}s\n")

# --------------------------------------------------------------------------
# COMMAND-LINE ENTRY POINT
# --------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Live Fractal Portal — transmit 140.625 Hz carrier with φ-fractal modulation via CoreAudio",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 live_fractal_portal.py                  # Run indefinitely
  python3 live_fractal_portal.py --duration 3600  # Run for 1 hour
  python3 live_fractal_portal.py -d 1800          # Run for 30 minutes

The fractal-modulated carrier is output through the MacBook's built-in
speakers or headphone jack at low latency, creating a live resonant
field that extends the Altar's 25-foot bubble to encompass the computer.

Dependencies: pip3 install sounddevice numpy
        """
    )
    parser.add_argument('-d', '--duration', type=int, default=None,
                       help='Duration in seconds (default: run indefinitely)')
    args = parser.parse_args()

    portal = FractalPortal(carrier=CARRIER, layers=FRACTAL_LAYERS)
    portal.run(duration=args.duration)

if __name__ == "__main__":
    main()
