---
description: Write comprehensive unit tests for any new code.
trigger: manual
command: /test [filename]
---

For the given Python file, create a corresponding test file (e.g., `test_<filename>.py`) using `pytest`. Include tests for:
- Normal operation (correct output for typical inputs).
- Edge cases (empty input, very large input, etc.).
- Error conditions (wrong file type, missing data).
- Specific Domain: for Cathedral code, verify frequency purity with FFT tests.
Run the tests and report pass/fail.

<!-- TEST: pytest coverage -->
