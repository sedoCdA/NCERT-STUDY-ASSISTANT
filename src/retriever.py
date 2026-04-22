import json
import numpy as np
from rank_bm25 import BM25Okapi

def load_chunks(chunks_path):
    # Load chunks.json and return list of chunk dicts
    with open(chunks_path, "r", encoding="utf-8") as f:
        chunks = json.load(f)
    return chunks

def build_index(chunks):
    # 1. Tokenize each chunk's text into words (lowercase)
    #    hint: chunk["text"].lower().split()
    tokenized_chunks = [chunk["text"].lower().split() for chunk in chunks]
    # 2. Build BM25Okapi index from tokenized chunks
    index = BM25Okapi(tokenized_chunks)
    # 3. Return the index
    return index

def retrieve(query, chunks, index, top_k=3):
    # 1. Tokenize the query the same way as chunks
    tokenized_query = query.lower().split()
    # 2. Get BM25 scores: index.get_scores(tokenized_query)
    scores = index.get_scores(tokenized_query)
    # 3. Get top_k chunk indices by score (hint: sorted + argsort)
    top_indices = np.argsort(scores)[::-1][:top_k]  # descending order
    # 4. Return top_k chunks as list of dicts
    return [chunks[i] for i in top_indices]

if __name__ == "__main__":
    chunks = load_chunks("data/processed/chunks.json")
    index = build_index(chunks)
    
    # Test with this query
    query = "What is the formula for acceleration?"
    results = retrieve(query, chunks, index, top_k=3)
    
    for i, chunk in enumerate(results):
        print(f"\n--- Result {i+1} ---")
        print(chunk["text"][:300])