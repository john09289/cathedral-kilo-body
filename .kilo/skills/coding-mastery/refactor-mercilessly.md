---
description: Refactor existing code to improve structure without changing functionality.
trigger: manual
command: /refactor [filename]
---

Given a file, apply the following refactorings:
- Extract long methods into smaller, named functions.
- Replace magic numbers with named constants from the King's frequency table.
- Remove duplicated code.
- Simplify nested conditionals using guard clauses or lookup tables.
Ensure all tests still pass. Commit the changes with a message like "♻️ Refactor: improve clarity without altering behavior."

<!-- REFACTOR: merciless but safe -->
