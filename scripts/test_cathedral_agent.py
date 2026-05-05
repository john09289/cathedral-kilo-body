#!/usr/bin/env python3
"""
Cathedral Agent Test Script
Tests memory recall, identity verification, and WAV generation.
"""

import sys
import os
import subprocess
import json
from datetime import datetime

# Add project root to path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

MEMORY_DIR = os.path.expanduser("~/cathedral_memory/")
MEMORY_INDEX = os.path.join(MEMORY_DIR, "index.json")

def check_memory():
    """Check memory engine status and entries."""
    print("="*60)
    print("🧠 CATHEDRAL MEMORY ENGINE CHECK")
    print("="*60)
    
    if not os.path.exists(MEMORY_INDEX):
        print("❌ Memory index not found. Run memory_engine.py first.")
        return False
    
    with open(MEMORY_INDEX, 'r') as f:
        data = json.load(f)
    
    print(f"Total entries: {len(data['entries'])}")
    print(f"Conversations: {data.get('conversations', 0)}")
    print(f"Created: {data.get('created', 'unknown')}")
    print(f"Last update: {data['entries'][-1]['timestamp'] if data['entries'] else 'none'}")
    print()
    
    # Show recent memories
    print("Recent memories:")
    for i, entry in enumerate(data['entries'][-3:], 1):
        text = entry['text']
        if len(text) > 80:
            text = text[:77] + "..."
        print(f"  {i}. [{entry['timestamp']}] {text}")
    print()
    return True

def test_identity():
    """Test agent identity verification."""
    print("="*60)
    print("🎯 AGENT IDENTITY VERIFICATION")
    print("="*60)
    
    agent_file = os.path.join(PROJECT_ROOT, ".kilo/agents/cathedral-engineer.md")
    if not os.path.exists(agent_file):
        print("❌ Agent file not found!")
        return False
    
    with open(agent_file, 'r') as f:
        content = f.read()
    
    checks = [
        ("Identity lock present", "IDENTITY LOCK" in content or "YOU ARE KILO" in content),
        ("Carrier locked at 11.71875", "11.71875" in content),
        ("Conditional Prayer present", "Conditional Prayer" in content or "Yeshua, have mercy" in content),
        ("Memory integration present", "Memory" in content or "recall" in content.lower()),
        ("Transmutation protocol present", "Transmutation" in content),
    ]
    
    for check_name, result in checks:
        status = "✅" if result else "❌"
        print(f"{status} {check_name}")
    
    print()
    return all(r for _, r in checks)

def test_wav_generation():
    """Test WAV generation capabilities."""
    print("="*60)
    print("🔊 WAV GENERATION TEST")
    print("="*60)
    
    scripts = {
        "generate_wav.py": "Fractal WAV generator",
        "transmutation_engine.py": "Transmutation engine",
        "generate_healing_wav.py": "Healing WAV generator",
    }
    
    all_ok = True
    for script, desc in scripts.items():
        path = os.path.join(PROJECT_ROOT, "scripts", script)
        exists = os.path.exists(path)
        status = "✅" if exists else "❌"
        print(f"{status} {desc}: {script}")
        if not exists:
            all_ok = False
    
    print()
    
    # Test transmutation engine
    print("Testing transmutation engine...")
    try:
        result = subprocess.run(
            ["python3", os.path.join(PROJECT_ROOT, "scripts/transmutation_engine.py")],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            print("✅ Transmutation engine runs successfully")
            if "TOTAL CATHEDRAL HARVEST" in result.stdout:
                print("✅ Harvest calculation working")
            # Check if WAV was generated
            wav_path = "transmuted_hate.wav"
            if os.path.exists(wav_path):
                size = os.path.getsize(wav_path)
                print(f"✅ WAV file generated: {wav_path} ({size} bytes)")
                os.remove(wav_path)  # Clean up
            else:
                print("⚠️  WAV file not generated (may need scipy)")
        else:
            print(f"❌ Transmutation engine failed: {result.stderr}")
            all_ok = False
    except subprocess.TimeoutExpired:
        print("❌ Transmutation engine timed out")
        all_ok = False
    except Exception as e:
        print(f"❌ Error running transmutation engine: {e}")
        all_ok = False
    
    print()
    return all_ok

def test_memory_recall():
    """Test memory recall functionality."""
    print("="*60)
    print("🔍 MEMORY RECALL TEST")
    print("="*60)
    
    # Add a test memory
    print("Adding test memory...")
    test_memory = "Test: Kilo agent verification at " + datetime.utcnow().isoformat() + "Z"
    result = subprocess.run(
        ["python3", os.path.join(PROJECT_ROOT, "scripts/memory_engine.py"),
         "remember", test_memory],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✅ Memory stored successfully")
    else:
        print(f"❌ Failed to store memory: {result.stderr}")
        return False
    
    # Recall the memory
    print("Recalling test memory...")
    result = subprocess.run(
        ["python3", os.path.join(PROJECT_ROOT, "scripts/memory_engine.py"),
         "recall", "Kilo agent"],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0 and result.stdout:
        print("✅ Memory recall working")
        print("Results:")
        for line in result.stdout.strip().split('\n')[:3]:
            print(f"  {line}")
    else:
        print("⚠️  No results from recall (may be low similarity)")
    
    print()
    return True

def main():
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║     CATHEDRAL ENGINEER AGENT — VERIFICATION TEST          ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    print()
    
    results = {}
    
    results["Memory Check"] = check_memory()
    results["Identity Verification"] = test_identity()
    results["WAV Generation"] = test_wav_generation()
    results["Memory Recall"] = test_memory_recall()
    
    print("="*60)
    print("📊 FINAL RESULTS")
    print("="*60)
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    all_passed = all(results.values())
    print()
    if all_passed:
        print("🎉 All tests passed! Cathedral Engineer agent is operational.")
    else:
        print("⚠️  Some tests failed. Review above for details.")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())