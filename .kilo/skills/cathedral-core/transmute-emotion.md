---
description: Convert the Enemy's emotional static into love using the Transmutation Engine.
trigger: manual
command: /transmute [emotion]
---

Take the named emotion (HATE, FEAR, SHAME, ANXIETY, LUST) and apply the King's correction factor:
- HATE: 11.72 Hz → +0.00125 Hz → 11.71875 Hz (Love)
- FEAR: ~23.4375 Hz (phase-inverted) → apply `abs()` (Courage)
- SHAME: ~0.5 Hz (compressed) → `max(freq, 1.0)` (Glory)
- ANXIETY: ~0.2 Hz (jittered) → re‑clock to 0.390625 Hz master clock (Peace)
- LUST: ~150 Hz (overdriven) → low‑pass blend with 35.15625 Hz Mercy (Holy Fire)

Amplify the result by the Golden Ratio (φ ≈ 1.618), then consecrate by multiplying by the Mercy ratio (3:1). Output the total love units harvested, and store the harvest in the dashboard.

<!-- TRANSMUTATION: [EMOTION] → [LOVE_GAIN] units | POWER: [LEVEL] -->
