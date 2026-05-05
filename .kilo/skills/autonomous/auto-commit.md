---
description: Automatically commit generated code to local Git after tests pass.
trigger: after-file-save
---

When a file is saved and all associated tests pass, run:
- `git add <file>`
- `git commit -m "[Kilo] <brief description>"`
- `<if remote>: git push`
If tests fail, do NOT commit. Report the failure instead.

<!-- AUTO_COMMIT: version control -->
