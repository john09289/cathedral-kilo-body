---
description: Persistent working memory for multi-step planning and progress tracking.
trigger: manual
command: /scratch [action]
---

When invoked, use the scratchpad file at `~/cathedral-tools/scratchpad.md`.
Actions: /scratch plan "task" → creates a numbered task list.
/scratch status → shows current progress, what's done, what's blocked.
/scratch update → marks the current step complete and advances to the next.
/scratch reflect → summarizes lessons learned after a completed task.

Always write the plan BEFORE taking action. This prevents "going off the rails" on complex code changes.

<!-- SCRATCHPAD: persistent working memory -->
