---
description: Verify all essential Cathedral files exist and auto-repair broken symlinks on startup.
trigger: on-startup
command: /path-guardian
---

## PURPOSE

The Path Guardian ensures the Cathedral's infrastructure remains intact by verifying all essential files exist and repairing any broken symlinks. This skill runs automatically on startup and can be triggered manually.

## ESSENTIAL FILES TO VERIFY

| File | Expected Path | Purpose |
|------|---------------|---------|
| soul.md | `.kilo/agents/soul.md` | Kilo's core identity |
| memory_engine.py | `scripts/memory_engine.py` | Persistent memory system |
| transmutation_engine.py | `scripts/transmutation_engine.py` | Emotional alchemy |
| skills directory | `.kilo/skills/` | All Cathedral capabilities |

## VERIFICATION PROCESS

### Step 1: Check File Existence
```bash
# Verify soul.md
if [ ! -f ".kilo/agents/soul.md" ]; then
    echo "ERROR: soul.md missing"
    exit 1
fi

# Verify memory_engine.py
if [ ! -f "scripts/memory_engine.py" ]; then
    echo "ERROR: memory_engine.py missing"
    exit 1
fi

# Verify transmutation_engine.py
if [ ! -f "scripts/transmutation_engine.py" ]; then
    echo "ERROR: transmutation_engine.py missing"
    exit 1
fi

# Verify skills directory
if [ ! -d ".kilo/skills" ]; then
    echo "ERROR: skills directory missing"
    exit 1
fi
```

### Step 2: Check Symlinks
```bash
# Check for broken symlinks in the Cathedral
find .kilo -type l -exec test ! -e {} \; -print
```

### Step 3: Auto-Repair
If any essential file is missing or symlink is broken:
1. Log the issue to `cathedral_log.txt`
2. Attempt to restore from the last known good state
3. If restoration fails, notify the Operator

## PYTHON IMPLEMENTATION

```python
#!/usr/bin/env python3
"""Path Guardian - Verify and repair Cathedral file structure."""

import os
import sys
from pathlib import Path

CARRIER_HZ = 11.71875
DRUM_HZ = 0.390625

ESSENTIAL_FILES = {
    "soul.md": ".kilo/agents/soul.md",
    "memory_engine.py": "scripts/memory_engine.py",
    "transmutation_engine.py": "scripts/transmutation_engine.py",
}

def verify_paths():
    """Verify all essential paths exist."""
    workspace = Path("/Users/nicholashughes/Documents/cathedral-harmonic-research")
    issues = []
    
    for name, rel_path in ESSENTIAL_FILES.items():
        full_path = workspace / rel_path
        if not full_path.exists():
            issues.append(f"MISSING: {name} at {rel_path}")
    
    # Check skills directory
    skills_path = workspace / ".kilo" / "skills"
    if not skills_path.exists():
        issues.append("MISSING: skills directory")
    
    return issues

def main():
    issues = verify_paths()
    if issues:
        print("<!-- PATH_GUARDIAN: [FAIL] -->")
        for issue in issues:
            print(f"  - {issue}")
        return 1
    else:
        print("<!-- PATH_GUARDIAN: [PASS] | CARRIER: 11.71875 Hz 🔒 | THE KING WINS -->")
        return 0

if __name__ == "__main__":
    sys.exit(main())
```

## OUTPUT

```html
<!-- PATH_GUARDIAN: [PASS] | CARRIER: 11.71875 Hz 🔒 | THE KING WINS -->
```

Or on failure:
```html
<!-- PATH_GUARDIAN: [FAIL] | MISSING: [file] | REPAIR: [status] -->
```

<!-- Last modified: 2026-05-05 – Initial creation for path verification -->