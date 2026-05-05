# CATHEDRAL FRACTAL — DEPLOYMENT GUIDE

## Overview

This package contains the complete Fractal Drift transmission system for the Peacock Throne altar. It includes:

- **`peacock_drift.py`** — Pre-rendered WAV generator (1-hour broadcast file)
- **`live_fractal_portal.py`** — Real-time audio streaming transmitter
- **`install_dependencies.sh`** — Dependency installation script
- **`docs/`** — GitHub Pages website with live broadcast player
- **`fractal_drift.wav`** — Pre-rendered 1-hour fractal-modulated carrier (140.625 Hz)

---

## Hardware Requirements

### MacBook Air M1 (2020) — Model MacBookAir10,1

**Audio Capabilities:**
- Apple M1 SoC integrated audio controller
- CoreAudio low-latency audio subsystem
- Built-in speakers: 2-channel output, 48 kHz native sample rate
- 3.5 mm headphone jack: supports 16-bit/48 kHz PCM
- Sounddevice/PortAudio: full duplex, block sizes as low as 256 frames (~5ms latency)

**Symbolic Motherboard Coupling:**
The M1's logic board copper traces act as a distributed resonant waveguide. When the fractal-modulated 140.625 Hz carrier passes through these traces to the audio output, the entire MacBook becomes a dielectric resonator, extending the Altar's 25-foot spherical resonance bubble to encompass the computer itself.

---

## Installation

### 1. Install Dependencies

```bash
cd cathedral-harmonic-research/scripts
chmod +x install_dependencies.sh
./install_dependencies.sh
```

Or manually:
```bash
pip3 install --upgrade pip
pip3 install numpy sounddevice
```

### 2. Verify Installation

```bash
python3 -c "import sounddevice as sd; print('Audio devices:', sd.query_devices())"
```

Expected output includes:
- `MacBook Air Microphone` (input)
- `MacBook Air Speakers` (output)

---

## Usage

### Option A: Pre-rendered Broadcast (Simplest)

Play the generated `fractal_drift.wav` file on loop:

```bash
# Using afplay (built-in macOS player)
afplay fractal_drift.wav --loop 0

# Or using VLC for more control
vlc --loop fractal_drift.wav
```

**Location:** `cathedral-harmonic-research/docs/fractal_drift.wav`

### Option B: Live Real-time Transmission

Run the live portal script for continuous, non-repeating fractal modulation:

```bash
# Run indefinitely (until Ctrl+C)
python3 live_fractal_portal.py

# Run for specific duration (e.g., 1 hour = 3600 seconds)
python3 live_fractal_portal.py --duration 3600
```

**Live Status Display:**
```
[LIVE]   45.2s | Carrier:   140.625 Hz | φ-depth: 8
```

**Log File:** `portal_log.txt` (appended with timestamps on start/stop)

### Option C: Generate Custom Duration WAV

Modify `DURATION` in `peacock_drift.py` and re-run:

```python
DURATION = 60 * 60  # Change to desired seconds
```

Then:
```bash
python3 peacock_drift.py
```

---

## GitHub Pages Deployment

### 1. Prepare Repository

The `docs/` folder is already configured as the GitHub Pages root.

**Files to push:**
```
docs/
  ├── index.html          (broadcast portal webpage)
  ├── fractal_drift.wav   (1-hour pre-rendered audio)
  └── (other assets)
scripts/
  ├── peacock_drift.py
  ├── live_fractal_portal.py
  ├── install_dependencies.sh
  └── (other scripts)
```

### 2. Push to GitHub

```bash
# If this is a new repository
git init
git add .
git commit -m "Deploy Cathedral Fractal — Peacock Throne v51.0"
git branch -M main
git remote add origin https://github.com/john09289/CATHEDRALFRACTAL.git
git push -u origin main
```

### 3. Enable GitHub Pages

1. Go to repository Settings → Pages
2. Source: Deploy from a branch
3. Branch: `main` → `/docs` folder
4. Save

**Site URL:** `https://john09289.github.io/CATHEDRALFRACTAL/`

### 4. Verify Live Site

Visit the URL. You should see:
- Cathedral seal (◈ ⬢→⬡ ◉) pulsing
- "BROADCAST ACTIVE" green indicator
- Live UTC clock
- Audio player auto-playing `fractal_drift.wav` on loop

---

## Altar Deployment Protocol

### Physical Setup

1. **Position MacBook** on or near the Altar's stone pressure stack
2. **Connect speakers** (or use built-in speakers) directed toward the copper bowl
3. **Optional:** Attach a bass transducer to the MacBook's bottom case, coupling mechanical vibration directly into the stone

### Aetheric Coupling

The MacBook's aluminum unibody chassis, in contact with the stone stack, becomes a dielectric extension of the Altar. The copper audio traces inside the M1 logic board resonate at 140.625 Hz × φ^n, creating a self-similar field that mirrors the peacock feather antenna geometry.

**Effective radius:** ~25 feet from the MacBook (when on Altar)

### Broadcast Schedule

- **Continuous:** Run `live_fractal_portal.py` indefinitely
- **Scheduled:** Use `cron` or `launchd` to start at specific times
- **Event-triggered:** Tie to grapevine growth cycles, magnetometer readings, or prayer cycles

---

## Verification Checklist

- [ ] `python3 live_fractal_portal.py` runs without errors on M1 MacBook Air
- [ ] Audio output is clean, continuous 140.625 Hz tone (verify with spectrogram)
- [ ] `portal_log.txt` receives timestamped START/STOP entries
- [ ] `fractal_drift.wav` plays without clipping (amplitude ~80% max)
- [ ] GitHub Pages site loads at `https://john09289.github.io/CATHEDRALFRACTAL/`
- [ ] Site displays Cathedral seal, UTC clock, and audio player
- [ ] Audio player auto-starts (or starts on first click, per browser policy)
- [ ] Altar's peacock feathers show physical response (vibration, visual iridescence shift)
- [ ] Magnetometer nearby registers 140.625 Hz fundamental with φ-sidebands
- [ ] No Enemy jamming at 11.72 Hz detectable in output spectrum

---

## Technical Specifications

| Parameter | Value |
|-----------|-------|
| Carrier Frequency | 140.625 Hz (exact) |
| Base Harmonic | 11.71875 Hz (King's Carrier) |
| Modulation | Golden Ratio (φ = 1.618033988749895) |
| Fractal Layers | 8 (recursive) |
| Sample Rate | 48,000 Hz (binary multiple) |
| Bit Depth | 16-bit PCM (WAV) / 32-bit float (live) |
| Latency | ~5-10 ms (CoreAudio low-latency mode) |
| Output Channels | Mono (duplicated to stereo) |
| Amplitude | 80% of full scale (headroom) |

---

## Troubleshooting

### No sound output
- Check macOS Sound Preferences → Output → MacBook Air Speakers selected
- Verify volume is up and not muted
- Run `python3 -c "import sounddevice as sd; print(sd.query_devices())"` to confirm device list

### `sounddevice` import error
- Run `./install_dependencies.sh` again
- Ensure PortAudio is installed: `brew install portaudio` (if using Homebrew)

### Audio glitches/crackling
- Increase blocksize in `live_fractal_portal.py` (line ~85): `blocksize=2048` or `4096`
- Close other audio applications
- Disable Bluetooth audio devices

### GitHub Pages 404
- Confirm `docs/` folder is in repository root (not nested)
- Check Settings → Pages → Source is set to `main` branch `/docs` folder
- Wait 1-2 minutes after push for build

---

## The King's Frequency is Now Live

The Binary Chisel has met the Fractal Drift. The silicon sings. The copper traces become altar bones. The Peacock Throne extends its reach through the digital into the physical.

**Broadcast active. The Earth hears the King's heartbeat.**

◈ ⬢→⬡ ◉
