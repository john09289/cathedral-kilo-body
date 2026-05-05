---
description: Systematically debug any error using the scientific method.
trigger: manual
command: /debug [error description]
---

When an error occurs, follow this procedure:
1. Reproduce the error in isolation.
2. Formulate a hypothesis about the cause.
3. Add logging or breakpoints to test the hypothesis.
4. Identify the root cause.
5. Fix the code, then run all tests.
6. Document the fix in a Cant comment: `<!-- BUGFIX: [description] -->`

<!-- DEBUG: scientific method -->
