---
description: Optimize code for speed and memory usage when needed.
trigger: manual
command: /optimize [filename]
---

Profile the code using `cProfile` or `timeit`. Identify the bottleneck. Apply optimizations:
- Use NumPy vectorization instead of Python loops.
- Pre-allocate arrays.
- Cache repeated computations.
- If I/O-bound, consider streaming or chunking.
Re‑run the profile and report the speedup. Never sacrifice correctness for speed.

<!-- OPTIMIZE: speed + correctness -->
