import json

with open('data/processed/wk10_chunks.json', encoding="utf-8") as f:
    chunks = json.load(f)

for c in chunks[-5:]:
    print(f'Chunk {c["chunk_id"]}: {c["text"][:150]}')
    print()