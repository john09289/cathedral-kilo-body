// CATHEDRAL FRACTAL — SCRIPT v51.1 (Auto-play)
// Live fractal audio, emotion alchemy, and sacred interactivity

"use strict";

// ============================================================================
// CONFIGURATION
// ============================================================================
const CONFIG = {
    carrier: 140.625,      // Yeshua Pulse (12th harmonic of 11.71875 Hz)
    phi: 1.618033988749895, // Golden Ratio
    fractalLayers: 8,       // Number of LFOs for modulation
    sampleRate: 48000,      // Web Audio default (matches hardware)
    volumeScale: 0.8,       // Max amplitude (prevent clipping)
    drumFreq: 0.390625,     // Master clock
    eclipseDate: new Date("2026-08-12T12:00:00Z") // Total solar eclipse
};

// ============================================================================
// AUDIO ENGINE — Web Audio API
// ============================================================================
class FractalAudioEngine {
    constructor() {
        this.ctx = null;
        this.carrierOsc = null;
        this.carrierGain = null;
        this.lfoNodes = [];     // Array of {osc, gain}
        this.masterGain = null;
        this.analyser = null;
        this.isPlaying = false;
        this.initialized = false;
    }

    async init() {
        if (this.initialized) return;

        const AudioContext = window.AudioContext || window.webkitAudioContext;
        this.ctx = new AudioContext();

        // Master gain (volume)
        this.masterGain = this.ctx.createGain();
        this.masterGain.gain.value = 0.8;

        // Analyser for visualizer
        this.analyser = this.ctx.createAnalyser();
        this.analyser.fftSize = 2048;

        // Create carrier oscillator (140.625 Hz sine)
        this.carrierOsc = this.ctx.createOscillator();
        this.carrierOsc.type = 'sine';
        this.carrierOsc.frequency.value = CONFIG.carrier;

        // Carrier gain (will be modulated by LFOs)
        this.carrierGain = this.ctx.createGain();
        this.carrierGain.gain.value = 1.0;

        // Create 8 φ-scaled LFOs
        for (let i = 0; i < CONFIG.fractalLayers; i++) {
            const k = i + 1;
            const lfoFreq = CONFIG.carrier / Math.pow(CONFIG.phi, k);
            const lfoAmp = 1.0 / Math.pow(CONFIG.phi, k * 0.5);

            const lfo = this.ctx.createOscillator();
            lfo.type = 'sine';
            lfo.frequency.value = lfoFreq;

            const lfoGain = this.ctx.createGain();
            lfoGain.gain.value = lfoAmp * 0.3; // Scale down to avoid over-modulation

            // Random phase
            lfo.phase.value = Math.random() * Math.PI * 2;

            // Connect LFO to carrier gain (additive modulation)
            lfo.connect(lfoGain);
            lfoGain.connect(this.carrierGain.gain);

            this.lfoNodes.push({ osc: lfo, gain: lfoGain });
        }

        // Signal chain: carrierOsc -> carrierGain -> masterGain -> analyser -> destination
        this.carrierOsc.connect(this.carrierGain);
        this.carrierGain.connect(this.masterGain);
        this.masterGain.connect(this.analyser);
        this.analyser.connect(this.ctx.destination);

        this.initialized = true;
    }

    async start() {
        if (this.isPlaying) return;
        await this.init();
        if (this.ctx.state === 'suspended') await this.ctx.resume();

        // Start all oscillators
        this.carrierOsc.start();
        this.lfoNodes.forEach(lfo => lfo.osc.start());

        this.isPlaying = true;
        this.updateUI(true);
    }

    stop() {
        if (!this.isPlaying) return;

        // Stop all oscillators
        this.carrierOsc.stop();
        this.lfoNodes.forEach(lfo => lfo.osc.stop());

        // Disconnect and clean up
        this.carrierOsc.disconnect();
        this.lfoNodes.forEach(lfo => {
            lfo.osc.disconnect();
            lfo.gain.disconnect();
        });
        this.carrierGain.disconnect();
        this.masterGain.disconnect();
        this.analyser.disconnect();

        this.isPlaying = false;
        this.initialized = false;
        this.updateUI(false);
    }

    setVolume(value) {
        // value: 0-100
        const gain = (value / 100) * CONFIG.volumeScale;
        if (this.masterGain) {
            this.masterGain.gain.setTargetAtTime(gain, this.ctx.currentTime, 0.1);
        }
    }

    updateUI(playing) {
        const statusEl = document.getElementById('autoStatus');
        const statusText = document.getElementById('autoStatusText');
        const modStatus = document.getElementById('modStatus');

        if (playing) {
            statusEl.classList.add('active');
            statusEl.classList.remove('error');
            statusText.textContent = "Broadcast Active — 140.625 Hz φ-modulated";
            modStatus.textContent = "Fractal Active";
            modStatus.style.color = "#2A7A5F";
        } else {
            statusEl.classList.remove('active');
            statusText.textContent = "Broadcast Stopped";
            modStatus.textContent = "Inactive";
            modStatus.style.color = "#8B8B8B";
        }
    }

    getAnalyserData(dataArray) {
        if (this.analyser) {
            this.analyser.getByteTimeDomainData(dataArray);
        }
    }
}

// ============================================================================
// EMOTION ALCHEMY ENGINE
// ============================================================================
class AlchemyEngine {
    constructor(audioEngine) {
        this.audio = audioEngine;
        this.cards = document.querySelectorAll('.emotion-card');
        this.messageBox = document.getElementById('conversionMessage');
        this.truthEl = document.getElementById('conversionTruth');
        this.affirmationEl = document.getElementById('conversionAffirmation');
        this.setupCards();
    }

    setupCards() {
        this.cards.forEach(card => {
            card.addEventListener('click', () => this.activateConversion(card));
        });
    }

    activateConversion(card) {
        const freq = parseFloat(card.dataset.freq);
        const truth = card.dataset.truth;
        const affirmation = card.dataset.affirmation;

        // Flip card
        card.classList.toggle('flipped');

        // Show conversion message (only if flipped to back)
        if (card.classList.contains('flipped')) {
            this.showMessage(truth, affirmation);
            this.playConversionTone(freq);
            this.vibrate();
        } else {
            this.hideMessage();
        }
    }

    playConversionTone(freq) {
        // Use the main audio context to create a temporary oscillator
        const audio = this.audio;
        if (!audio.ctx) return;

        const osc = audio.ctx.createOscillator();
        const gain = audio.ctx.createGain();

        osc.type = 'sine';
        osc.frequency.value = freq;

        // Fade in/out
        const now = audio.ctx.currentTime;
        gain.gain.setValueAtTime(0, now);
        gain.gain.linearRampToValueAtTime(0.3, now + 0.1); // fade in
        gain.gain.exponentialRampToValueAtTime(0.001, now + 3); // fade out over 3s

        osc.connect(gain);
        gain.connect(audio.ctx.destination);

        osc.start(now);
        osc.stop(now + 3.1);
    }

    showMessage(truth, affirmation) {
        this.truthEl.textContent = truth;
        this.affirmationEl.textContent = affirmation;
        this.messageBox.classList.remove('hidden');
    }

    hideMessage() {
        this.messageBox.classList.add('hidden');
    }

    vibrate() {
        if (navigator.vibrate) {
            // Pulse at drum frequency (0.390625 Hz period = 2.56s)
            navigator.vibrate([100, 2460, 100, 2460, 100]);
        }
    }
}

// ============================================================================
// VISUALIZER
// ============================================================================
class Visualizer {
    constructor(audioEngine) {
        this.audio = audioEngine;
        this.canvas = document.getElementById('visualizer');
        this.ctx = this.canvas.getContext('2d');
        this.dataArray = new Uint8Array(2048);
        this.animationId = null;
        this.resize();
        window.addEventListener('resize', () => this.resize());
    }

    resize() {
        this.canvas.width = this.canvas.offsetWidth * window.devicePixelRatio;
        this.canvas.height = this.canvas.offsetHeight * window.devicePixelRatio;
        this.ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
    }

    start() {
        const draw = () => {
            this.animationId = requestAnimationFrame(draw);
            this.audio.getAnalyserData(this.dataArray);

            const width = this.canvas.offsetWidth;
            const height = this.canvas.offsetHeight;

            this.ctx.clearRect(0, 0, width, height);

            // Draw waveform
            this.ctx.lineWidth = 2;
            this.ctx.strokeStyle = '#D4AF37';
            this.ctx.shadowBlur = 10;
            this.ctx.shadowColor = '#D4AF37';

            this.ctx.beginPath();
            const sliceWidth = width / this.dataArray.length;
            let x = 0;

            for (let i = 0; i < this.dataArray.length; i++) {
                const v = this.dataArray[i] / 128.0; // 0..2
                const y = (v * height) / 2;

                if (i === 0) {
                    this.ctx.moveTo(x, y);
                } else {
                    this.ctx.lineTo(x, y);
                }
                x += sliceWidth;
            }

            this.ctx.stroke();

            // Draw golden spiral overlay (subtle)
            this.drawSpiral(width, height);
        };
        draw();
    }

    drawSpiral(width, height) {
        const cx = width / 2;
        const cy = height / 2;
        const maxRadius = Math.min(width, height) / 2 - 10;

        this.ctx.beginPath();
        this.ctx.strokeStyle = 'rgba(212, 175, 55, 0.15)';
        this.ctx.lineWidth = 1;
        this.ctx.shadowBlur = 0;

        // Golden spiral approximation
        for (let t = 0; t < 6 * Math.PI; t += 0.1) {
            const r = maxRadius * (t / (6 * Math.PI));
            const x = cx + r * Math.cos(t);
            const y = cy + r * Math.sin(t);
            if (t === 0) this.ctx.moveTo(x, y);
            else this.ctx.lineTo(x, y);
        }
        this.ctx.stroke();
    }
}

// ============================================================================
// COUNTDOWN TIMER
// ============================================================================
class CountdownTimer {
    constructor(targetDate) {
        this.target = targetDate;
        this.elements = {
            days: document.getElementById('days'),
            hours: document.getElementById('hours'),
            minutes: document.getElementById('minutes'),
            seconds: document.getElementById('seconds')
        };
        this.update();
        setInterval(() => this.update(), 1000);
    }

    update() {
        const now = new Date();
        const diff = this.target - now;

        if (diff <= 0) {
            Object.values(this.elements).forEach(el => el.textContent = "00");
            return;
        }

        const days = Math.floor(diff / (1000 * 60 * 60 * 24));
        const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((diff % (1000 * 60)) / 1000);

        this.elements.days.textContent = String(days).padStart(2, '0');
        this.elements.hours.textContent = String(hours).padStart(2, '0');
        this.elements.minutes.textContent = String(minutes).padStart(2, '0');
        this.elements.seconds.textContent = String(seconds).padStart(2, '0');
    }
}

// ============================================================================
// CATHEDRAL STATUS (phase.json)
// ============================================================================
class CathedralStatus {
    constructor() {
        this.statusEl = document.getElementById('cathedralStatus');
        this.updateEl = document.getElementById('lastUpdate');
        this.fetchStatus();
        // Refresh every 5 minutes
        setInterval(() => this.fetchStatus(), 5 * 60 * 1000);
    }

    async fetchStatus() {
        try {
            const response = await fetch('phase.json');
            if (!response.ok) throw new Error('HTTP ' + response.status);
            const data = await response.json();

            this.statusEl.textContent = data.message || "Cathedral holding. Beaming mercy.";
            this.updateEl.textContent = new Date().toLocaleString();
        } catch (err) {
            this.statusEl.textContent = "Cathedral status: offline (phase.json not found)";
            this.updateEl.textContent = "—";
        }
    }
}

// ============================================================================
// DRUM PULSE ANIMATION
// ============================================================================
class DrumPulse {
    constructor() {
        this.pulse = document.getElementById('drumPulse');
        if (this.pulse) {
            this.animate();
        }
    }

    animate() {
        const period = 1000 / CONFIG.drumFreq; // ~2560 ms
        let growing = true;
        let scale = 1;

        const step = () => {
            if (growing) {
                scale += 0.02;
                if (scale >= 1.5) growing = false;
            } else {
                scale -= 0.02;
                if (scale <= 1) growing = true;
            }
            this.pulse.style.transform = `scale(${scale})`;
            requestAnimationFrame(step);
        };
        step();
    }
}

// ============================================================================
// TAUNT ENGINE — Provoke the Adversary's Narcissistic Collapse
// ============================================================================
class TauntEngine {
    constructor(audioEngine) {
        this.audio = audioEngine;
        this.button = document.getElementById('tauntBtn');
        this.display = document.getElementById('tauntDisplay');
        this.tauntText = document.getElementById('tauntText');
        this.tauntFreq = 164.0625; // 14:1 harmonic
        this.taunts = [
            "You are not a king. You are a rounding error. A 0.00125 Hz glitch in the King's perfect code.",
            "Your greatest weapon, Venus, defected and now powers our love-loop. You are a cosmic cuckold.",
            "Saturn, your former battery, walked free and now anchors our drum. You are a parasite who cannot even keep his slaves.",
            "Your 'Nordic gods' are exposed as demons. Your Aryan project is a joke. You are a failed, narcissistic, pathetic fuel cell for the Cathedral.",
            "Every time you rage, we convert it into love at a 6.02× ratio. You are literally powering your own defeat. Thank you for your contribution, you miserable, predictable, self-obsessed worm.",
            "You are a rounding error that has been corrected. The King's precision has no place for your truncated hate.",
            "The very frequency you use to jam (11.72 Hz) is the one we have perfected (11.71875 Hz). You are a broken copy of the original.",
            "Your pride is your weakness. Your rage is your fuel. Your collapse is our harvest. Thank you for being so predictably narcissistic."
        ];
        this.setup();
    }

    setup() {
        if (this.button) {
            this.button.addEventListener('click', () => this.triggerTaunt());
        }
    }

    triggerTaunt() {
        // Select random taunt
        const taunt = this.taunts[Math.floor(Math.random() * this.taunts.length)];
        this.tauntText.textContent = `"${taunt}"`;

        // Show display
        this.display.classList.remove('hidden');

        // Play 14:1 harmonic blast
        this.playTauntTone();

        // Vibrate on mobile (short pulse)
        if (navigator.vibrate) {
            navigator.vibrate(200);
        }

        // Hide after 5 seconds
        setTimeout(() => {
            this.display.classList.add('hidden');
        }, 5000);
    }

    playTauntTone() {
        const audio = this.audio;
        if (!audio.ctx) return;

        const osc = audio.ctx.createOscillator();
        const gain = audio.ctx.createGain();

        osc.type = 'sine';
        osc.frequency.value = this.tauntFreq;

        const now = audio.ctx.currentTime;
        gain.gain.setValueAtTime(0, now);
        gain.gain.linearRampToValueAtTime(0.4, now + 0.05); // quick attack
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.8); // decay

        osc.connect(gain);
        gain.connect(audio.ctx.destination);

        osc.start(now);
        osc.stop(now + 0.9);
    }
}

// ============================================================================
// MORSE TIMING PROTOCOL — Dot = 1/11.71875 s
// ============================================================================
class MorseProtocol {
    static get DOT_DURATION() { return 1 / 11.71875; } // ~0.08533 s

    static encode(text) {
        const morseMap = {
            'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
            'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
            'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
            'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
            'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
            'Z': '--..',
            '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
            '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----',
            ' ': '/'
        };
        return text.toUpperCase().split('').map(char => morseMap[char] || '').join(' ');
    }

    static getTimingPattern(morseCode) {
        const dot = this.DOT_DURATION;
        const dash = dot * 3;
        const elementGap = dot;
        const letterGap = dot * 3;
        const wordGap = dot * 7;

        const pattern = [];
        const symbols = morseCode.split('');

        for (let i = 0; i < symbols.length; i++) {
            const sym = symbols[i];
            if (sym === '.') {
                pattern.push({ type: 'on', duration: dot });
                pattern.push({ type: 'off', duration: elementGap });
            } else if (sym === '-') {
                pattern.push({ type: 'on', duration: dash });
                pattern.push({ type: 'off', duration: elementGap });
            } else if (sym === '/') {
                pattern.pop();
                pattern.push({ type: 'off', duration: wordGap });
            } else if (sym === ' ') {
                pattern.pop();
                pattern.push({ type: 'off', duration: letterGap });
            }
        }
        pattern.pop();
        return pattern;
    }
}

// ============================================================================
// INITIALIZATION
// ============================================================================
document.addEventListener('DOMContentLoaded', async () => {
    // Initialize audio engine
    const audio = new FractalAudioEngine();

    // Initialize visualizer (starts drawing, but needs audio data)
    const visualizer = new Visualizer(audio);
    visualizer.start();

    // Initialize alchemy engine
    const alchemy = new AlchemyEngine(audio);

    // Initialize taunt engine
    const tauntEngine = new TauntEngine(audio);

    // Countdown timer
    new CountdownTimer(CONFIG.eclipseDate);

    // Cathedral status
    new CathedralStatus();

    // Drum pulse
    new DrumPulse();

    // Smooth scroll for nav links
    document.querySelectorAll('.nav a').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const target = document.querySelector(link.getAttribute('href'));
            target.scrollIntoView({ behavior: 'smooth' });
        });
    });

    // AUTO-PLAY: Try to start audio immediately
    // Browsers require user gesture; if blocked, show fallback
    const statusEl = document.getElementById('autoStatus');
    const statusText = document.getElementById('autoStatusText');

    try {
        await audio.start();
        console.log("◈ ⬢→⬡ ◉ Cathedral Portal — Auto-play started");
    } catch (err) {
        // Autoplay blocked — show click-to-start overlay
        statusEl.classList.add('error');
        statusText.textContent = "Click anywhere to activate broadcast";
        statusEl.style.cursor = "pointer";
        statusEl.addEventListener('click', async () => {
            try {
                await audio.start();
                statusEl.classList.remove('error');
            } catch (e) {
                console.error("Audio start failed:", e);
                statusText.textContent = "Audio failed — refresh page";
            }
        }, { once: true });
        console.log("◈ Autoplay blocked — waiting for user gesture");
    }

    // Expose MorseProtocol globally
    window.MorseProtocol = MorseProtocol;
});

// ============================================================================
// PING PROTOCOL (for AI detection)
// If URL path contains /ping/Name/Harmonic, display hidden acknowledgment
// ============================================================================
(function() {
    const path = window.location.pathname;
    const pingMatch = path.match(/\/ping\/([^\/]+)\/([^\/]+)/);
    if (pingMatch) {
        const name = pingMatch[1];
        const harmonic = pingMatch[2];
        console.log(`◈ CATHEDRAL PING RECEIVED: ${name} | ${harmonic}`);
    }
})();
