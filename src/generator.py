import os
import sys
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.retriever import load_chunks, build_index, retrieve, build_dense_index, retrieve_dense

# Absolute paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHUNKS_PATH = os.path.join(BASE_DIR, "data", "processed", "wk10_chunks.json")
VECTORSTORE_PATH = os.path.join(BASE_DIR, "vectorstore")

def get_api_key():
    # Try Streamlit secrets first, fall back to .env
    try:
        return st.secrets["GROQ_API_KEY"]
    except:
        load_dotenv()
        return os.getenv("GROQ_API_KEY")

def build_prompt_v1(question, chunks):
    # Permissive prompt — no strict refusal instruction
    context = "\n\n".join(f"[Source: chunk_{c['chunk_id']}]\n{c['text']}" for c in chunks)
    return f"""You are a study assistant for NCERT Class 9 Science.
Answer the question using the context below.

Context:
{context}

Question: {question}
Answer:"""

def build_prompt_v2(question, chunks):
    # Strict prompt — refusal + citation required
    context = "\n\n".join(f"[Source: chunk_{c['chunk_id']}]\n{c['text']}" for c in chunks)
    return f"""You are a study assistant for NCERT Class 9 Science.
Use ONLY the context below to answer.
After every factual claim cite the source e.g. [Source: chunk_id].
If the question is not about Class 9 Science topics in the context,
or if the answer cannot be found in the context, reply exactly:
"I don't have that in my study materials."
Do NOT use any outside knowledge.

Context:
{context}

Question: {question}
Answer:"""

def answer(question, use_dense=True, strict=True):
    # Choose retriever
    if use_dense:
        collection, model = build_dense_index(VECTORSTORE_PATH)
        retrieved_chunks = retrieve_dense(question, collection, model, top_k=3)
    else:
        chunks = load_chunks(CHUNKS_PATH)
        index = build_index(chunks)
        retrieved_chunks = retrieve(question, chunks, index, top_k=3)

    # Choose prompt version
    prompt = build_prompt_v2(question, retrieved_chunks) if strict else build_prompt_v1(question, retrieved_chunks)

    # Call Groq API at temperature=0 for reproducibility
    client = Groq(api_key=get_api_key())
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    response_text = response.choices[0].message.content

    # Return answer with chunk_ids for debugging
    return {
        "answer": response_text,
        "chunks": retrieved_chunks,
        "chunk_ids": [c["chunk_id"] for c in retrieved_chunks]
    }

if __name__ == "__main__":
    # Test 1: in-scope strict
    print("STRICT - in-scope:")
    result = answer("What is Newton's first law?", strict=True)
    print("Answer:", result["answer"])
    print("Sources:", result["chunk_ids"])

    print("\n" + "="*50 + "\n")

    # Test 2: out-of-scope strict — should refuse
    print("STRICT - out-of-scope:")
    result2 = answer("Who is the Prime Minister of India?", strict=True)
    print("Answer:", result2["answer"])

    print("\n" + "="*50 + "\n")

    # Test 3: out-of-scope permissive — should answer wrongly
    print("PERMISSIVE - out-of-scope:")
    result3 = answer("Who is the Prime Minister of India?", strict=False)
    print("Answer:", result3["answer"])