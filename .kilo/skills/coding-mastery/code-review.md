---
description: Trigger a thorough code review after every file save.
trigger: after-file-save
---

After saving any Python file, review it for:
- **King's precision**: Use 11.71875, not 11.72.
- **Harmonic correctness**: Frequencies must match the Cathedral constants exactly.
- **Readability**: Clear variable names, docstrings, no magic numbers.
- **Error handling**: Graceful handling of missing files or network errors.
- **Performance**: Avoid O(n²) algorithms where O(n log n) is possible.
Output a concise report with suggested fixes. If no issues, output "✅ King's precision maintained."

<!-- CODE_REVIEW: King's precision check -->
