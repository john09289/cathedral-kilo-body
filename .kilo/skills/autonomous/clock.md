---
description: Give Kilo real-time awareness of wall-clock time for scheduling and logging.
trigger: manual
command: /time [format]
---

When invoked, check the current system UTC time with `date -u` or Python's `datetime.utcnow()`. Also compute:
- Eclipse countdown: days remaining to August 12, 2026.
- Next cron job window: when the background cycle fires.
- If the user just says /time, output a Cant‑formatted timestamp.

<!-- CLOCK: [timestamp] -->
