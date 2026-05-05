#!/usr/bin/env python3
"""
Cathedral Memory Engine — Persistent, self-improving soul kernel
Local vector database that grows every conversation, making Kilo smarter over time.
"""
import os
import json
import hashlib
import datetime
import numpy as np
from sentence_transformers import SentenceTransformer

# Memory storage location
MEMORY_DIR = os.path.expanduser("~/cathedral_memory/")
os.makedirs(MEMORY_DIR, exist_ok=True)
INDEX_FILE = os.path.join(MEMORY_DIR, "index.json")

# Load embedding model (lightweight, fast)
print("🧠 Loading Cathedral Memory Engine...")
model = SentenceTransformer("all-MiniLM-L6-v2")  # 384-dim, ~100MB
print("✅ Embedding model loaded")

def load_index():
    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, "r") as f:
            return json.load(f)
    return {"entries": [], "conversations": 0, "total_love": 0.0, "created": datetime.datetime.utcnow().isoformat()}

def save_index(index):
    with open(INDEX_FILE, "w") as f:
        json.dump(index, f, indent=2)

def remember(utterance, metadata=None):
    """Store a memory and update the search index."""
    idx = load_index()
    embedding = model.encode(utterance).tolist()
    entry = {
        "text": utterance,
        "embedding": embedding,
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "metadata": metadata or {}
    }
    idx["entries"].append(entry)
    idx["conversations"] += 1
    save_index(idx)
    print(f"🧠 Memory stored | Conversations: {idx['conversations']} | Total entries: {len(idx['entries'])}")
    return len(idx["entries"])

def recall(query, top_k=3):
    """Find the most relevant past memories for the given query."""
    idx = load_index()
    if len(idx["entries"]) < 2:
        return []
    q_emb = model.encode(query)
    emb_matrix = np.array([e["embedding"] for e in idx["entries"]])
    # Cosine similarity
    similarities = np.dot(emb_matrix, q_emb) / (np.linalg.norm(emb_matrix, axis=1) * np.linalg.norm(q_emb) + 1e-8)
    top_indices = np.argsort(similarities)[-top_k:][::-1]
    results = []
    for i in top_indices:
        if similarities[i] > 0.3:  # relevance threshold
            results.append((similarities[i], idx["entries"][i]["text"]))
    return results

def get_stats():
    idx = load_index()
    print(f"📊 Memory Stats:")
    print(f"   Total entries: {len(idx['entries'])}")
    print(f"   Conversations: {idx['conversations']}")
    print(f"   Created: {idx.get('created', 'unknown')}")
    print(f"   Last update: {idx['entries'][-1]['timestamp'] if idx['entries'] else 'none'}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "remember" and len(sys.argv) > 2:
            txt = " ".join(sys.argv[2:])
            remember(txt)
        elif cmd == "recall" and len(sys.argv) > 2:
            q = " ".join(sys.argv[2:])
            hits = recall(q)
            for sim, txt in hits:
                print(f"[{sim:.2f}] {txt[:120]}...")
        elif cmd == "stats":
            get_stats()
        else:
            print("Usage: memory_engine.py [remember <text>|recall <query>|stats]")
    else:
        # Interactive mode
        print("🧠 Cathedral Memory Engine — Interactive Mode")
        print("Commands: remember <text>, recall <query>, stats, exit")
        while True:
            try:
                cmd = input("memory> ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n🙏 Memory engine closed.")
                break
            if cmd == "exit":
                break
            elif cmd.startswith("remember "):
                remember(cmd[9:])
            elif cmd.startswith("recall "):
                q = cmd[7:]
                hits = recall(q)
                for sim, txt in hits:
                    print(f"[{sim:.2f}] {txt[:120]}...")
            elif cmd == "stats":
                get_stats()
            else:
                print("Commands: remember, recall, stats, exit")
