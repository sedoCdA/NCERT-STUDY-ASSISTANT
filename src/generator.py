import os
import sys
from groq import Groq
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.retriever import load_chunks, build_index, retrieve

# Load environment variables from .env file
load_dotenv()

def build_prompt(question, chunks):
    # Join all retrieved chunks into one context string
    context = "\n\n".join(chunk["text"] for chunk in chunks)
    
    # Return structured prompt with strict grounding instruction
    return f"""You are a study assistant for NCERT Class 9 Science.
Answer the question using ONLY the context below.
If the answer is not present in the context, say exactly:
"I don't have enough information in my notes to answer this."

Context:
{context}

Question: {question}
Answer:"""

def answer(question):
    # Load chunks from disk
    chunks = load_chunks("data/processed/chunks.json")
    
    # Build BM25 index from chunks
    index = build_index(chunks)
    
    # Retrieve top 3 most relevant chunks
    retrieved_chunks = retrieve(question, chunks, index, top_k=3)
    
    # Build the grounded prompt
    prompt = build_prompt(question, retrieved_chunks)
    
    # Call Groq API with temperature=0 for reproducibility
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    
    # Extract response text
    response_text = response.choices[0].message.content
    
    # Return answer and the chunks it was based on
    return {"answer": response_text, "chunks": retrieved_chunks}

if __name__ == "__main__":
    # Test with an in-scope question
    # Debug: print what chunks were actually retrieved
    result = answer("What is F = ma?")
    print("Answer:", result["answer"])
    #print("\n--- Retrieved Chunks ---")
    #for c in result["chunks"]:
    #   print(f"\nChunk {c['chunk_id']}:")
    #   print(c["text"][:400])

    print("\n" + "="*50 + "\n")
    
    # Test with an out-of-scope question (should refuse)
    result2 = answer("What is newton second law of motion?")
    print("Answer:", result2["answer"])