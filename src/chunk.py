import json
import os
import re
import tiktoken

def get_content_type(text):
    # Detect worked examples by "Example" followed by a number
    if re.search(r'Example\s+\d+', text):
        return "worked_example"
    # Detect exercises by keyword or question mark at end
    if "EXERCISES" in text or text.strip().endswith("?"):
        return "question_or_exercise"
    # Everything else is prose
    return "prose"

def count_tokens(text):
    # cl100k_base is the tokenizer used by GPT-4 and embeddings
    enc = tiktoken.get_encoding("cl100k_base")
    return len(enc.encode(text))

def split_into_chunks(text, chunk_size=250, overlap=50):
    # Encode entire text into tokens
    enc = tiktoken.get_encoding("cl100k_base")
    tokens = enc.encode(text)
    chunks = []
    start = 0

    while start < len(tokens):
        # Slice token window
        end = start + chunk_size
        chunk_tokens = tokens[start:end]
        # Decode tokens back to text
        chunk_text = enc.decode(chunk_tokens)
        chunks.append(chunk_text)
        # Slide forward with overlap
        start += chunk_size - overlap

    return chunks

def chunk_chapter(chapter_data):
    chapter_id = chapter_data["chapter"]
    text = chapter_data["text"]
    chunk_texts = split_into_chunks(text)

    return [
        {
            "chapter": chapter_id,
            "chunk_id": i,
            "text": chunk_text,
            "content_type": get_content_type(chunk_text),
            "token_count": count_tokens(chunk_text)
        }
        for i, chunk_text in enumerate(chunk_texts)
    ]

def chunk_all(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as f:
        extracted_data = json.load(f)

    all_chunks = []
    for chapter_data in extracted_data:
        chunks = chunk_chapter(chapter_data)
        all_chunks.extend(chunks)

    # Print summary
    print(f"Total chunks: {len(all_chunks)}")
    for ct in ["prose", "worked_example", "question_or_exercise"]:
        count = sum(1 for c in all_chunks if c["content_type"] == ct)
        print(f"  {ct}: {count}")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2, ensure_ascii=False)

    print(f"Saved to {output_path}")

if __name__ == "__main__":
    chunk_all("data/processed/extracted.json",
              "data/processed/wk10_chunks.json")