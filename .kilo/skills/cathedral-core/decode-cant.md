---
description: Extract hidden Cant messages from a WAV file.
trigger: manual
command: /decode [filename]
---

Read the given WAV file, analyze the 140.625 Hz carrier for small frequency deviations (±0.5 Hz), and decode the hidden binary message. Output the decoded text. If no message is found, report "No Cant detected."

<!-- DECODE_CANT -->
