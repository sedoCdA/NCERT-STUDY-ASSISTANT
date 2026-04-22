import json
import os

def split_into_chunks(text, chunk_size=250, overlap=50):
    # 1. Split text into words and store in a list
    words = text.split()
    chunks = []

    # 2. Use a sliding window:
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk_words = words[start:end]
        # 3. Join words back into a string for each chunk
        chunk_text = " ".join(chunk_words)
        chunks.append(chunk_text)
        start += chunk_size - overlap
    
    # 4. Return list of chunk strings
    return chunks

def chunk_chapter(chapter_data):
    # 1. Get chapter id and text from chapter_data dict
    chapter_id = chapter_data["chapter"]
    text = chapter_data["text"]

    # 2. Call split_into_chunks() on the text
    chunk_texts = split_into_chunks(text)
    
    # 3. Return list of dicts:
    #    {"chapter": chapter_id, "chunk_id": i, "text": chunk_text}
    return [{"chapter": chapter_id, "chunk_id": i, "text": chunk_text} for i, chunk_text in enumerate(chunk_texts)]

def chunk_all(input_path, output_path):
    # 1. Load extracted.json
    with open(input_path, "r", encoding="utf-8") as f:
        extracted_data = json.load(f)
    # 2. For each chapter, call chunk_chapter()
    all_chunks = []
    for chapter_data in extracted_data:
        chunks = chunk_chapter(chapter_data)
        all_chunks.extend(chunks)

    # 3. Print how many chunks were created
    print(f"Total chunks created: {len(all_chunks)}")

    # 4. Save all chunks to data/processed/chunks.json
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2, ensure_ascii=False)

    
if __name__ == "__main__":
    # Define input and output paths
    input_path = "data/processed/extracted.json"
    output_path = "data/processed/chunks.json"
    
    chunk_all(input_path, output_path)
    print(f"Chunks saved to {output_path}")