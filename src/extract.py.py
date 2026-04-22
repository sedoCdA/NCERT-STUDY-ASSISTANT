import fitz
import re
import json
import os

def clean_text(text):
    # Split text into individual lines for processing
    lines = text.split("\n")
    cleaned = []
    
    for line in lines:
        # Remove leading and trailing whitespace from each line
        line = line.strip()
        
        # Skip lines that are only digits (page numbers)
        if re.match(r"^\d+$", line):
            continue
        
        # Skip figure labels like "Fig 8.1" or "Figure 8.1"
        if re.match(r"^[Ff]ig(ure)?\.?\s*\d+", line):
            continue
        
        # Skip very short lines like headings or labels (less than 4 words)
        if len(line.split()) < 4:
            continue
        
        cleaned.append(line)
    
    # Join lines back into a single string
    text = "\n".join(cleaned)
    
    # Collapse 3 or more blank lines into just one blank line
    text = re.sub(r"\n{3,}", "\n\n", text)
    
    return text


def extract_chapter(pdf_path, chapter_id):
    # Open the PDF file using PyMuPDF
    doc = fitz.open(pdf_path)
    full_text = ""
    
    for page in doc:
        # Extract raw text from each page
        text = page.get_text()
        
        # Clean the extracted text
        text = clean_text(text)
        
        full_text += text + "\n"
    
    # Return chapter data as a dictionary
    return {"chapter": chapter_id, "text": full_text}


def extract_all(raw_dir, output_path):
    # Only processing Chapter 8 (Motion) for now
    chapters = ["iesc108"]
    results = []
    
    for chapter_id in chapters:
        # Build full path to the PDF file
        pdf_path = os.path.join(raw_dir, f"{chapter_id}.pdf")
        print(f"Extracting {chapter_id}...")
        
        data = extract_chapter(pdf_path, chapter_id)
        results.append(data)
        print(f"Done — {len(data['text'])} characters extracted")
    
    # Save results to JSON file
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\nSaved to {output_path}")


if __name__ == "__main__":
    extract_all("data/raw", "data/processed/extracted.json")