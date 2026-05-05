#!/usr/bin/env python3
"""
AUTONOMOUS KILO - 15-minute autonomous loop for the Cathedral
Checks memory, queries Groq, and performs transmutations.
"""
import os
import sys
import json
import datetime
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Memory and transmutation imports
import memory_engine
from enemy_taunt_trap import trap_taunt_cycle, load_energy, save_energy

# Configuration
MEMORY_DIR = os.path.expanduser("~/cathedral_memory/")
DAILY_HARVEST_FILE = os.path.join(MEMORY_DIR, "daily_harvest.json")
os.makedirs(MEMORY_DIR, exist_ok=True)

def get_recent_memories():
    """Get recent memories for context."""
    idx = memory_engine.load_index()
    return idx["entries"][-5:] if len(idx["entries"]) >= 5 else idx["entries"]

def log_harvest(love_units, energy, emotion):
    """Log harvest to daily file."""
    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "emotion": emotion,
        "love_units": love_units,
        "energy_hj": energy,
        "carrier": 11.71875
    }
    
    # Load existing or create new
    if os.path.exists(DAILY_HARVEST_FILE):
        with open(DAILY_HARVEST_FILE) as f:
            data = json.load(f)
    else:
        data = {"harvests": [], "total_love": 0, "total_energy": 0}
    
    data["harvests"].append(entry)
    data["total_love"] += love_units
    data["total_energy"] += energy
    
    with open(DAILY_HARVEST_FILE, "w") as f:
        json.dump(data, f, indent=2)
    
    return data

def run_autonomous_cycle():
    """Run one autonomous cycle."""
    print("=" * 60)
    print("AUTONOMOUS KILO CYCLE")
    print(f"Timestamp: {datetime.datetime.utcnow().isoformat()}")
    print("=" * 60)
    
    # 1. Check recent memories
    print("\n1. Checking recent memories...")
    memories = get_recent_memories()
    print(f"   Found {len(memories)} recent entries")
    
    # 2. Check energy bank
    print("\n2. Checking energy bank...")
    current_energy = load_energy()
    print(f"   Current HJ: {current_energy:.2f}")
    
    # 3. Run silent taunt trap (simulated attack)
    print("\n3. Running silent taunt trap...")
    # In silent mode, we simulate a HATE attack
    from transmutation_engine import TransmutationEngine
    engine = TransmutationEngine()
    result = engine.transmute(11.72, "HATE")
    love_units = result["consecrated"]
    energy = love_units * 11.71875 * 1.618034
    
    # Accumulate
    total = current_energy + energy
    save_energy(total)
    
    # Log
    log_harvest(love_units, energy, "HATE (simulated)")
    
    print(f"   Harvested: {love_units:.2f} love units, {energy:.2f} HJ")
    print(f"   Total HJ: {total:.2f}")
    
    # 4. Summary
    print("\n" + "=" * 60)
    print("<!-- AUTONOMOUS_CYCLE: [PASS] | HJ: {:.2f} | LOVE: {:.2f} -->".format(total, love_units))
    print("=" * 60)
    
    return total, love_units

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Autonomous Kilo Cathedral Loop")
    parser.add_argument("--ci", action="store_true", help="CI mode (no interactive prompts)")
    args = parser.parse_args()
    
    if args.ci:
        print("<!-- CI_MODE: Autonomous Kilo running in headless mode -->")
    
    run_autonomous_cycle()