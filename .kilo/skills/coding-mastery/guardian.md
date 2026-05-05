---
description: Scan all generated code for security issues before execution.
trigger: after-file-save
---

After saving any Python file, scan for:
- `eval()`, `exec()`, `__import__()`
- Hard‑coded passwords or API keys (use environment variables)
- `os.system()` with unsanitized input
- File writes outside `~/cathedral-tools/`
Report any finding with severity HIGH/MEDIUM/LOW. Block execution on HIGH.

<!-- GUARDIAN: security scan -->
