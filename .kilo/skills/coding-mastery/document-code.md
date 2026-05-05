---
description: Ensure every public function has a clear docstring and a usage example.
trigger: manual
command: /doc [filename]
---

Scan the file for any function without a docstring. Add a Google‑style docstring that includes:
- A brief description.
- Parameters (name, type, meaning).
- Returns (type, description).
- A usage example in a doctest format.
If the function is part of the Cathedral, include a Cant comment reference.

<!-- DOC: Google style -->
