---
description: Process many files at once (e.g., encoding all WAVs in a directory).
trigger: manual
command: /batch [operation] [directory]
---

Given an operation (e.g., encode Cant, apply Watcher filter, generate spectrum) and a directory, iterate over all matching files and apply the operation. Use multiprocessing if beneficial. Log progress and errors. Summarize results at the end.

<!-- BATCH: process all -->
