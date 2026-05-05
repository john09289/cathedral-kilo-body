---
description: Write code using strict Test-Driven Development (TDD).
trigger: manual
command: /tdd [feature]
---

When asked to implement a feature, follow TDD precisely:
1. Write a failing test that describes the desired behavior.
2. Run the test to confirm it fails.
3. Write the simplest possible code to make the test pass.
4. Run the test again—all tests must pass.
5. Refactor: improve the code structure without changing behavior, ensuring tests still pass.
Repeat for each new behavior. Every public function must have at least one test.

<!-- TDD: RED → GREEN → REFACTOR -->
