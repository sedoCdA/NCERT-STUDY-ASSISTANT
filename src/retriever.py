import json
import numpy as np
from rank_bm25 import BM25Okapi

import chromadb
from sentence_transformers import SentenceTransformer

def build_dense_index(vectorstore_path):
    # Load ChromaDB client from vectorstore folder
    client = chromadb.PersistentClient(path=vectorstore_path)
    
    # Load the same collection we created in embed.py
    collection = client.get_collection(name="ncert_chunks")
    
    # Load the same embedding model
    model = SentenceTransformer("all-MiniLM-L6-v2")
    
    return collection, model

def retrieve_dense(query, collection, model, top_k=3):
    # 1. Embed the query using the same model
    query_embedding = model.encode(query).tolist()
    
    # 2. Query ChromaDB for most similar chunks
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    
    # 3. Format results same way as BM25 retrieve()
    chunks = []
    for i in range(len(results["documents"][0])):
        chunks.append({
            "chunk_id": results["ids"][0][i],
            "text": results["documents"][0][i],
            "chapter": results["metadatas"][0][i]["chapter"]
        })
    
    return chunks

if __name__ == "__main__":
    # Test dense retrieval
    collection, model = build_dense_index("vectorstore")
    
    results = retrieve_dense("What is the definition of momentum?", collection, model)
    for i, chunk in enumerate(results):
        print(f"\n--- Result {i+1} (Chunk {chunk['chunk_id']}) ---")
        print(chunk["text"][:300])