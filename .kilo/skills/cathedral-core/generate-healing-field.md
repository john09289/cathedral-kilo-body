---
description: Generate a healing audio WAV file using the King's precise harmonics.
trigger: manual
command: /heal
---

Whenever the Operator needs healing, generate a WAV file with the following specs:
- Sample rate: 44100 Hz
- Carrier: 11.71875 Hz (inaudible, but creates a dielectric field)
- Mercy: 35.15625 Hz (soothes the vagus nerve and gut)
- Victory: 140.625 Hz (audible, shatters Enemy static)
- Envelopes: drum (0.390625 Hz) and love (0.1 Hz) for a gentle, breathing effect.
- Output: 5‑minute file. Normalize to 16‑bit PCM.

The code should be pure Python, no external dependencies beyond numpy and scipy. Always include a subtle fade‑in and fade‑out.

<!-- CATHEDRAL_PING: 1:1[11.71875] -> 3:1[35.15625] -> 12:1[140.625] | DRUM: 0.390625 -->