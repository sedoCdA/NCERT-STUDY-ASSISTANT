# add temporarily to debug_chunks.py
import json
with open('data/processed/chunks.json', encoding="utf-8") as f:
    chunks = json.load(f)

for c in chunks:
    if 'momentum' in c['text'].lower():
        print(f"Chunk {c['chunk_id']}: {c['text'][:200]}")
        print('---')