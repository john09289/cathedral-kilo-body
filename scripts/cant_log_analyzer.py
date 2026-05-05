#!/usr/bin/env python3
"""
CANT LOG ANALYZER — Harvests all Cant HTML comments from the codebase
Compiles a unified chronicle of the Cathedral's work.
"""
import os
import re

def harvest_cant_comments(root_dir="."):
    cant_pattern = re.compile(r'<!--\s*(.*?)\s*-->', re.DOTALL)
    harvest = []
    keywords = ['king', 'cathedral', 'cant', 'victory', 'carrier', 'mercy', 
                'pulse', 'drum', 'love', 'eclipse', 'jamming', 'transmutation']
    
    for dirpath, _, filenames in os.walk(root_dir):
        # Skip hidden dirs
        if any(hidden in dirpath for hidden in ['.git', '__pycache__', 'node_modules']):
            continue
        for filename in filenames:
            if filename.endswith(('.py', '.md', '.txt', '.html', '.json', '.sh')):
                filepath = os.path.join(dirpath, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        matches = cant_pattern.findall(content)
                        for match in matches:
                            if any(kw in match.lower() for kw in keywords):
                                harvest.append((filename, match.strip()))
                except:
                    pass
    
    print(f"📜 HARVESTED CANT COMMENTS: {len(harvest)} found\n")
    print("=" * 60)
    for filename, comment in harvest:
        print(f"[{filename}]")
        print(f"  {comment[:150]}")
        print()
    print("=" * 60)
    print(f"Total Cant entries: {len(harvest)}")
    return harvest

if __name__ == "__main__":
    harvest_cant_comments(SCRIPT_DIR if 'SCRIPT_DIR' in dir() else '.')
