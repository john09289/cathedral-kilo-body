---
description: Check code for security vulnerabilities common in Python.
trigger: manual
command: /secure [filename]
---

Review the file for:
- Use of `eval()` or `exec()`.
- Hard‑coded passwords (use environment variables).
- Unsanitized user input (command injection, path traversal).
- Unvalidated data from external sources.
Report any findings with severity. For Cathedral code, ensure all API keys are loaded from environment variables.

<!-- SECURITY: no eval, env vars only -->
