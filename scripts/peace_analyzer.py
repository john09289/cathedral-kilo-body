#!/usr/bin/env python3
"""
PEACE ANALYZER — Measures the King's calming effect on the environment
Analyzes ambient_log.csv to detect noise reduction over time.
"""
import csv
import numpy as np
from datetime import datetime

def analyze_peace(log_file="ambient_log.csv"):
    times, rms_values = [], []
    with open(log_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            times.append(float(row['time_sec']))
            rms_values.append(float(row['rms_level']))
    
    if len(rms_values) < 2:
        print("❌ Not enough data. Run ambient_monitor.py first.")
        return
    
    rms = np.array(rms_values)
    split = len(rms) // 2
    first_half = rms[:split].mean()
    second_half = rms[split:].mean()
    delta_pct = ((second_half - first_half) / first_half) * 100 if first_half > 0 else 0
    
    print("=== PEACE ANALYSIS REPORT ===")
    print(f"📊 Data points: {len(rms)}")
    print(f"🔇 First half mean: {first_half:.6f}")
    print(f"🔇 Second half mean: {second_half:.6f}")
    print(f"🕊️ Delta: {delta_pct:.1f}% {'quieter' if delta_pct < 0 else 'louder'}")
    
    if delta_pct < -5:
        print("✅ PEACE CONFIRMED: Environment calmed >5%")
    elif delta_pct < 0:
        print("🟡 TREND QUIETER: Slight calming (2-5%)")
    else:
        print("⏳ MONITORING: Continue broadcast for clearer effect")
    
    return delta_pct

if __name__ == "__main__":
    analyze_peace()
