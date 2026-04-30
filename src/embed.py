import chromadb
from sentence_transformers import SentenceTransformer
import json
import os

def embed_and_store(chunks_path, vectorstore_path):
    # Load wk10 chunks
    with open(chunks_path, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    # Load embedding model
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Create ChromaDB client
    client = chromadb.PersistentClient(path=vectorstore_path)

    # Delete old collection if exists to avoid conflicts
    try:
        client.delete_collection(name="ncert_chunks")
        print("Deleted old collection")
    except:
        pass

    # Create fresh collection
    collection = client.get_or_create_collection(name="ncert_chunks")

    # Embed and store each chunk with content_type in metadata
    for chunk in chunks:
        embedding = model.encode(chunk["text"])
        collection.add(
            ids=[str(chunk["chunk_id"])],
            embeddings=[embedding.tolist()],
            documents=[chunk["text"]],
            metadatas=[{
                "chapter": chunk["chapter"],
                "content_type": chunk["content_type"],
                "token_count": chunk["token_count"]
            }]
        )

    print(f"Embedded and stored {len(chunks)} chunks in ChromaDB")

if __name__ == "__main__":
    embed_and_store("data/processed/wk10_chunks.json", "vectorstore")