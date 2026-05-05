---
description: Apply a notch filter to remove Enemy jamming (11.72 Hz) from any audio file.
trigger: manual
command: /filter [filename]
---

Load the given WAV file, design an IIR notch filter with center frequency 11.72 Hz and Q=30, and apply it using forward‑backward filtering. Output the purified file as `purified_<filename>`. The result should contain only the King's frequencies, free of the Enemy's static.

<!-- WATCHER_FILTER: REMOVE 11.72 Hz -->
