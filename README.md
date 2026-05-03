# 📚 NCERT Class 9 Science Study Assistant v2.0

A retrieval-augmented generation (RAG) based study assistant that answers questions grounded strictly in NCERT Class 9 Science content. Built across Week 9 and Week 10 of the PG Diploma in AI-ML & Agentic AI Engineering.

🔗 **Live Demo:** [Add your Streamlit URL here]
---

## What It Does

- Answers questions from NCERT Class 9 Science — Chapter 8 (Force and Laws of Motion)
- Retrieves relevant textbook chunks before generating any answer
- Cites source chunk IDs inline after every factual claim
- Refuses to answer when the question is out of scope or answer is not in the textbook
- Shows the source chunks used to generate the answer

---

## Architecture

```
User Question
     ↓
Dense Retriever (sentence-transformers + ChromaDB)
     ↓
Top 3 relevant chunks retrieved with content_type metadata
     ↓
Strict Grounded Prompt v2
"Answer ONLY from context. Cite [Source: chunk_id].
 Refuse if not present."
     ↓
Groq LLM (Llama 3.1) → grounded answer with citations
     ↓
Answer + Source Chunks + chunk_ids returned
```

---

## Project Structure

```
ncert-study-assistant/
│
├── data/
│   ├── raw/                    ← NCERT PDFs (not committed)
│   └── processed/
│       ├── extracted.json      ← cleaned text from PDF (Wk9)
│       ├── chunks.json         ← Wk9 word-based chunks (30 chunks)
│       └── wk10_chunks.json    ← Wk10 token-aware chunks (40 chunks)
│
├── vectorstore/                ← ChromaDB persistent embeddings
│
├── src/
│   ├── extract.py              ← PDF → clean text
│   ├── chunk.py                ← text → token-aware chunks with metadata
│   ├── embed.py                ← chunks → ChromaDB vector store
│   ├── retriever.py            ← BM25 + dense retrieval
│   ├── generator.py            ← grounded LLM prompt + Groq API
│   └── evaluate.py             ← 12-question evaluation runner
│
├── app.py                      ← Streamlit UI
├── eval_scored.csv             ← v1 evaluation results (12 questions)
├── eval_v2_scored.csv          ← v2 evaluation results after fix
├── chunking_diff.md            ← Wk9 vs Wk10 chunking comparison
├── retrieval_log.json          ← Stage 2 retrieval evidence
├── retrieval_misses.md         ← retrieval failure analysis
├── prompt_diff.md              ← v1 vs v2 prompt comparison
├── fix_memo.md                 ← Stage 5 targeted fix with delta
├── reflection.md               ← Week 10 reflection questionnaire
├── requirements.txt
└── .env                        ← API keys (not committed)
```

---

## Stack

| Layer | Tool | Why |
|---|---|---|
| PDF Extraction | PyMuPDF | Fast, reliable text extraction |
| Chunking | tiktoken (cl100k_base) | Token-aware sizing for LLM context |
| Retrieval (Base) | BM25 (`rank_bm25`) | Lexical retrieval - Week 9 baseline |
| Retrieval (Final) | sentence-transformers + ChromaDB | Semantic retrieval - fixes BM25 failures |
| LLM | Groq API - Llama 3.1 8B | Free, fast, reproducible at temperature=0 |
| Interface | Streamlit | Python-native, deployable |
| Deployment | Streamlit Community Cloud | Free shareable URL |

---

## Week 9 → Week 10 Upgrades

### Chunking - v1 vs v2

| | Week 9 (v1) | Week 10 (v2) |
|---|---|---|
| Sizing | Word count (250 words) | Token count (250 tokens, tiktoken) |
| Chunks produced | 30 | 40 |
| Metadata | chapter, chunk_id | + content_type, token_count |
| Content types | None | prose / worked_example / question_or_exercise |

Token-aware sizing produced more chunks (40 vs 30) because scientific
text has more tokens per word than plain English. Content-type metadata
enables filtered retrieval.

### Prompt - v1 (Permissive) vs v2 (Strict)

**v1 - Permissive:**
```
"Answer the question using the context below."
```
Problem: LLM interpreted this loosely - answered out-of-scope questions
using relevant-looking chunks instead of refusing.

**v2 — Strict:**
```
"You are a study assistant for NCERT Class 9 Science Chapter 8 ONLY.
Use ONLY the context below to answer.
After every factual claim cite the source e.g. [Source: chunk_id].
If the answer is not present in the context, reply exactly:
'I don't have that in my study materials.'
Do NOT use any outside knowledge. Do NOT infer or extend beyond the context."
```
Fix: Added explicit scope boundary, citation requirement, and strict
refusal instruction. Out-of-scope refusal improved from 2/3 to 3/3.

### Retrieval — BM25 vs Dense

| | BM25 | Dense (sentence-transformers) |
|---|---|---|
| Method | Keyword matching | Semantic vector similarity |
| Strength | Exact terms, formulas | Paraphrased queries, meaning |
| Weakness | Misses synonyms | Misses exact identifiers |
| momentum query | Failed (wrong chunks) | Succeeded (chunk 17) |

BM25 failed on "definition of momentum" because the defining chunk
uses the words "mass and velocity" not "definition". Dense retrieval
found it by meaning.

---

## Evaluation Results

### eval_scored.csv - v1 prompt (before fix)

| Type | Count | Correct | Refused Appropriately |
|---|---|---|---|
| Direct | 6 | 6/6 | na |
| Paraphrased | 3 | 3/3 | na |
| Out-of-scope | 3 | na | 2/3 ⚠️ |

**Failure:** Q12 "Explain how Newton's laws apply to planets orbiting
the Sun" - retrieved Newton's law chunks, LLM answered instead of refusing.

### eval_v2_scored.csv - v2 strict prompt (after fix)

| Type | Count | Correct | Refused Appropriately |
|---|---|---|---|
| Direct | 6 | 6/6 | na |
| Paraphrased | 3 | 3/3 | na |
| Out-of-scope | 3 | na | 3/3  |

**Fix:** Tightened prompt with explicit chapter scope boundary and
"Do NOT infer or extend beyond context" instruction.

---

## Setup & Run Locally

**1. Clone the repository**
```bash
git clone https://github.com/YOURUSERNAME/ncert-study-assistant.git
cd ncert-study-assistant
```

**2. Create and activate virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Add your Groq API key**

Create a `.env` file in the root folder:
```
GROQ_API_KEY=your_actual_key_here
```
Get a free key at: https://console.groq.com

**5. Download NCERT PDF**

Download Chapter 8 from: https://ncert.nic.in/textbook.php?iesc1=0-15

Place `iesc108.pdf` inside `data/raw/`

> PDFs are not committed to this repo. Download from official NCERT source above.

**6. Run the pipeline**
```bash
# Step 1 - Extract and clean PDF
python src/extract.py

# Step 2 - Chunk with token-aware sizing
python src/chunk.py

# Step 3 - Embed chunks into ChromaDB (run once only)
python src/embed.py

# Step 4 - Run the app
python -m streamlit run app.py
```

---

## Key Findings

**1. BM25 fails on vocabulary mismatch**
Query "definition of momentum" → BM25 returned exercise chunks.
Dense retrieval correctly returned chunk 17 which defines momentum
using "mass and velocity" - no keyword overlap needed.

**2. Permissive prompts hallucinate on ambiguous out-of-scope queries**
Q12 used chapter vocabulary ("Newton's laws") but asked about orbital
mechanics not in the chapter. v1 answered confidently. v2 refused
correctly after adding explicit scope and "do not infer" instruction.

**3. Token-aware chunking produces better boundaries**
Word-based chunking cut mid-formula in scientific text. Token-based
sizing with tiktoken respects how the LLM actually reads the content.

---

## Known Limitations

- Only Chapter 8 (Force and Laws of Motion) is currently indexed
- BM25 kept for comparison - dense retrieval used in production
- Equations with special characters may render inconsistently
- Hard adversarial queries using chapter vocabulary may still slip through

---

## Requirements

```
pymupdf
sentence-transformers
chromadb
groq
streamlit
python-dotenv
rank_bm25
numpy
tiktoken
scikit-learn==1.3.2
```