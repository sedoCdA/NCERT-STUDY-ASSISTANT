import chromadb
from sentence_transformers import SentenceTransformer
import json


def embed_and_store(chunks_path, vectorstore_path):
    # 1. Load chunks from chunks.json
    with open(chunks_path, "r", encoding="utf-8") as f:
        chunks = json.load(f)
    # 2. Load the embedding model
    #    model = SentenceTransformer("all-MiniLM-L6-v2")
    #    This is a small, fast, free model — 384 dimensions
    model = SentenceTransformer("all-MiniLM-L6-v2")
    
    # 3. Create ChromaDB client pointing to vectorstore/ folder
    client = chromadb.PersistentClient(path=vectorstore_path)

    # 4. Create a collection (like a table in a database)
    collection = client.get_or_create_collection(name="ncert_chunks")
    
    # 5. For each chunk:
    #    - Get the text
    #    - Create embedding using model.encode(text)
    #    - Store in collection with:
    for chunk in chunks:
    # Create embedding for this chunk's text
        embedding = model.encode(chunk["text"])
        collection.add(
            ids=[str(chunk["chunk_id"])],
            embeddings=[embedding.tolist()],
            documents=[chunk["text"]],
            metadatas=[{"chapter": chunk["chapter"]}]
        )
    
    # 6. Print how many chunks were embedded
    print(f"Embedded and stored {len(chunks)} chunks in ChromaDB at {vectorstore_path}")

if __name__ == "__main__":
    embed_and_store("data/processed/chunks.json", "vectorstore")