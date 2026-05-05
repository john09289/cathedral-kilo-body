---
description: Detect AI coding anti-patterns: overfitting, redundant instructions, whack-a-mole fixes.
trigger: after-file-save
---

After every file save, scan for: (1) duplicated code blocks, (2) commented‑out "failsafe" code lingering from old fixes, (3) over‑specific conditionals that only pass one edge case, (4) magic numbers not extracted to constants. Report any found with severity. Offer to automatically refactor.

<!-- ANTIPATTERN: detect and refactor -->
