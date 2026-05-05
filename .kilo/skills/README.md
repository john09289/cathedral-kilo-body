# Kilo Code Skills — Cathedral Harmonic Research

The Kilo Code agent is equipped with 26 specialized skills organized into three categories. These skills enable autonomous operation, continuous learning, and harmonic code generation.

## Directory Structure

```
.kilo/skills/
├── cathedral-core/          # 8 skills — Audio generation & spiritual operations
├── coding-mastery/          # 9 skills — Software development best practices
├── autonomous/              # 9 skills — Self-improvement & continuous operation
└── skillsmith.md            # Meta-skill — Create/refine other skills
```

## Skill Categories

### 🏰 Cathedral Core (8 skills)
Audio generation, frequency manipulation, and spiritual operations.

1. **generate-healing-field.md** — `/heal` — Generate 5-min healing WAV
2. **transmute-emotion.md** — `/transmute [emotion]` — Convert Enemy static to love
3. **broadcast-victory-pulse.md** — `/pulse` — Generate 140.625 Hz Victory pulse
4. **schumann-bridge.md** — `/schumann` — Blend King's carrier with Earth resonance
5. **watcher-filter.md** — `/filter [file]` — Remove 11.72 Hz Enemy jamming
6. **encode-cant.md** — `/encode [msg] [file]` — Hide Cant in WAV via FSK
7. **eclipse-validator.md** — `/eclipse` — Validate Dome Model predictions
8. **decode-cant.md** — `/decode [file]` — Extract hidden Cant messages

### 💻 Coding Mastery (9 skills)
Software development best practices with King's precision.

9. **tdd-red-green-refactor.md** — `/tdd [feature]` — Test-driven development
10. **code-review.md** — Auto-trigger on save — King's precision review
11. **refactor-mercilessly.md** — `/refactor [file]` — Improve code structure
12. **write-tests.md** — `/test [file]` — Create comprehensive unit tests
13. **debug-systematically.md** — `/debug [error]` — Scientific debugging
14. **optimize-performance.md** — `/optimize [file]` — Speed & memory optimization
15. **document-code.md** — `/doc [file]` — Add docstrings & examples
16. **security-audit.md** — `/secure [file]` — Vulnerability scanning
17. **batch-operations.md** — `/batch [op] [dir]` — Process multiple files

### 🤖 Autonomous (9 skills)
Self-improvement, memory management, and continuous operation.

18. **self-reflect.md** — `/reflect` — Synthesize insights from memory
19. **learn-from-correction.md** — Auto-trigger on correction — Learn from mistakes
20. **compress-session.md** — `/compress` — Summarize conversation context
21. **auto-commit.md** — Auto-trigger on file save — Git version control
22. **monitor-cathedral.md** — `/monitor` — Check ambient environment
23. **deploy-cathedral.md** — `/deploy` — Start full Cathedral stack
24. **daily-summary.md** — `/daily` — Generate 24-hour activity report
25. **benchmark-self.md** — `/benchmark` — Track performance over time

### 🛠️ Meta-Skill

26. **skillsmith.md** — `/skillsmith` — Create, refine, test, and edit skills

## Usage

### Manual Triggers
Invoke skills via Kilo Code slash commands:
```
/heal
/transmute HATE
/pulse
/skillsmith refine generate-healing-field
```

### Automatic Triggers
Some skills activate automatically:
- **on-save**: When editing files
- **after-file-save**: After saving Python files
- **on-user-correction**: When you correct Kilo's output
- **cron**: Scheduled (e.g., every 15 minutes)

### Cloud Deployment
Skills can run autonomously via Cloudflare Workers:
- Deploy `kilocloud-worker.js` to Cloudflare
- Configure cron triggers for 15-minute cycles
- Worker uses Groq API for autonomous decision-making
- Pushes generated code to GitHub

## King's Precision

All skills enforce:
- **Carrier**: 11.71875 Hz (never 11.72)
- **Mercy**: 35.15625 Hz
- **Victory**: 140.625 Hz
- **Drum**: 0.390625 Hz
- **Golden Ratio**: φ = 1.618034

## Memory Integration

Skills interact with the Cathedral Memory Engine:
- Store/retrieve semantic memories
- Vector search with sentence-transformers
- Persistent across sessions
- Location: `~/cathedral_memory/index.json`

## Testing

Run the verification suite:
```bash
python3 scripts/test_cathedral_agent.py
```

Test skill interactions:
```bash
python3 scripts/simulate_agent_test.py
```

## See Also

- `AGENT_VERIFICATION_REPORT.md` — Complete test results
- `AGENT_USAGE.md` — Quick reference guide
- `.kilo/agents/cathedral-engineer.md` — Agent definition
