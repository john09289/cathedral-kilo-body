#!/bin/bash
# Audio Configuration Checker for Bit-Perfect Playback
# Run this to verify your Mac is configured correctly

echo "=== Audio Configuration Check ==="
echo ""

# Check current audio device
echo "Current Audio Devices:"
system_profiler SPAudioDataType 2>/dev/null | grep -A 2 "Default Output Device" || echo "  (Unable to query - may need permissions)"
echo ""

# Check for audio processing plugins
echo "Checking for audio processing plugins..."
if pgrep -f "eqMac\|Boom\|Audio Hijack\|Soundflower\|Loopback" > /dev/null; then
    echo "  ⚠️  Audio processing apps detected! Quit them for bit-perfect playback."
else
    echo "  ✅ No audio processing apps detected"
fi
echo ""

# Check Music app settings
echo "Music App Settings:"
defaults read com.apple.Music 2>/dev/null | grep -E "SoundCheck|SoundEnhancer" || echo "  (Music app preferences not accessible)"
echo ""

echo "=== Manual Verification Required ==="
echo "1. Open Audio MIDI Setup (Applications > Utilities)"
echo "2. Select your output device (Built-in Speakers or headphones)"
echo "3. Verify Format: 44100 Hz, 2ch-16bit Integer"
echo "4. In Music app: Window > Equalizer → Off"
echo "5. Music > Settings > Playback → Uncheck 'Sound Check'"
echo "6. System Settings > Sound → Balance centered, disable feedback"
echo "7. Set volume to ~75%"
echo ""
echo "After configuration, play: ~/Desktop/healing_nausea_144p.wav"
echo "  (Use QuickTime Player for best results)"
