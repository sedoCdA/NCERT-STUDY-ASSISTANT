import json
import numpy as np
from rank_bm25 import BM25Okapi
import chromadb
from sentence_transformers import SentenceTransformer

def load_chunks(chunks_path):
    # Load chunks from JSON file
    with open(chunks_path, "r", encoding="utf-8") as f:
        chunks = json.load(f)
    return chunks

def build_index(chunks):
    # Tokenize each chunk into lowercase words for BM25
    tokenized_chunks = [chunk["text"].lower().split() for chunk in chunks]
    index = BM25Okapi(tokenized_chunks)
    return index

def retrieve(query, chunks, index, top_k=3):
    # Tokenize query same way as chunks
    tokenized_query = query.lower().split()
    scores = index.get_scores(tokenized_query)
    top_indices = np.argsort(scores)[::-1][:top_k]
    return [chunks[i] for i in top_indices]

def build_dense_index(vectorstore_path):
    # Load ChromaDB client and embedding model
    client = chromadb.PersistentClient(path=vectorstore_path)
    collection = client.get_collection(name="ncert_chunks")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    return collection, model

def retrieve_dense(query, collection, model, top_k=3):
    # Embed query and search ChromaDB
    query_embedding = model.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    chunks = []
    for i in range(len(results["documents"][0])):
        chunks.append({
            "chunk_id": results["ids"][0][i],
            "text": results["documents"][0][i],
            "chapter": results["metadatas"][0][i]["chapter"],
            "content_type": results["metadatas"][0][i].get("content_type", "prose")
        })
    return chunks

if __name__ == "__main__":
    # Test dense retrieval
    collection, model = build_dense_index("vectorstore")
    results = retrieve_dense("What is the definition of momentum?", collection, model)
    for i, chunk in enumerate(results):
        print(f"\n--- Result {i+1} (Chunk {chunk['chunk_id']}) ---")
        print(chunk["text"][:300])