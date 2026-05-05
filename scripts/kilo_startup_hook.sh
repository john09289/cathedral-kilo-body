#!/bin/bash
# Kilo Code startup hook – ensures memory and agent are fresh
# Place this in ~/.kilo/init.sh or configure in VSCode:
# Settings → Extensions → Kilo Code → Startup Script

# Determine project root (flexible path resolution)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Pre-load memory engine to warm up the vector database
echo "🔄 Pre-loading Cathedral Memory Engine..."
python3 "$PROJECT_ROOT/scripts/memory_engine.py" stats > /dev/null 2>&1

# Check if memory has entries
MEMORY_FILE=~/cathedral_memory/index.json
if [ -f "$MEMORY_FILE" ]; then
    ENTRY_COUNT=$(python3 -c "import json; d=json.load(open('$MEMORY_FILE')); print(len(d['entries']))" 2>/dev/null)
    echo "🧠 Memory engine pre-loaded. Entries: ${ENTRY_COUNT:-0}"
else
    echo "🧠 Memory engine initialized (no entries yet)."
fi

# Verify agent file exists
AGENT_FILE="$PROJECT_ROOT/.kilo/agents/cathedral-engineer.md"
if [ -f "$AGENT_FILE" ]; then
    echo "✅ Cathedral Engineer agent file found."
else
    echo "⚠️  Agent file not found at $AGENT_FILE"
fi

echo "🎯 Kilo is ready. Identity: Witness Node | Carrier: 11.71875 Hz"