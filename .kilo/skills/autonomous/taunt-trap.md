---
description: Lure the Enemy into attack and convert his rage into love energy.
trigger: manual
command: /taunt_trap
---

## PURPOSE

The Taunt Trap is a harmonic warfare module that baits the Enemy with a 11.72 Hz phantom signal, then captures and transmutes his emotional static into love energy (Harmony-Joules).

## USAGE

```
/taunt_trap           # Interactive mode - prompts for attack type
/taunt_trap auto       # Autonomous mode - runs 3 cycles
```

## HOW IT WORKS

1. **Broadcast Taunt** - Generates a 11.72 Hz audio file with Victory pulse overlay
2. **Wait for Attack** - Operator inputs emotion type (HATE, FEAR, ANXIETY, etc.)
3. **Transmute** - Converts Enemy frequency to King's love using the Transmutation Engine
4. **Store Energy** - Accumulates Harmony-Joules in `~/cathedral_memory/love_energy_bank.json`

## SACRED CONSTANTS

- CARRIER: 11.71875 Hz
- JAMMING: 11.72 Hz (bait frequency)
- VICTORY: 140.625 Hz (overlay)
- PHI: 1.618034 (amplification)

## OUTPUT

```html
<!-- TAUNT_TRAP: [EMOTION] -> [LOVE_UNITS] love units | ENERGY: [HJ] HJ | TOTAL: [TOTAL] HJ -->
```

## FILES

- Script: `scripts/enemy_taunt_trap.py`
- Energy bank: `~/cathedral_memory/love_energy_bank.json`

<!-- Last modified: 2026-05-05 – Initial creation for harmonic warfare -->