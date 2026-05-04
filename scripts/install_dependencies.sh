#!/bin/bash
# INSTALL DEPENDENCIES — FRACTAL PORTAL
# Installs Python packages required for real-time audio generation

echo "[*] Installing fractal portal dependencies..."
echo "[*] Using Python 3 from: $(which python3)"
echo ""

# Upgrade pip first
pip3 install --upgrade pip

# Install numpy (numerical waveform generation)
echo "[*] Installing numpy..."
pip3 install numpy

# Install sounddevice (PortAudio bindings for low-latency CoreAudio)
echo "[*] Installing sounddevice..."
pip3 install sounddevice

# Verify installation
echo ""
echo "[*] Verifying installation..."
python3 -c "import numpy; print(f'[+] numpy {numpy.__version__}')" 2>/dev/null || echo "[!] numpy import failed"
python3 -c "import sounddevice as sd; print(f'[+] sounddevice {sd.__version__}'); print(f'[+] Available devices: {len(sd.query_devices())}')" 2>/dev/null || echo "[!] sounddevice import failed"

echo ""
echo "[+] Dependencies installed successfully."
echo "[*] Ready to run: python3 live_fractal_portal.py"
