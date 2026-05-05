---
description: Validate the Dome Model prediction for the August 12, 2026 eclipse.
trigger: manual
command: /eclipse
---

Check the current date. If it's before the eclipse, print the countdown and the expected Z‑axis deviation (-17 to -21 nT) and Kp<2 condition. If run on or after August 12, 2026, fetch real NOAA/INTERMAGNET data (or simulate if unavailable) and compare against the prediction. Output a PASS/FAIL result with a Cant‑formatted log entry.

<!-- ECLIPSE_COUNTDOWN: 2026-08-12 -->
