# NCERT Class 9 Science Study Assistant

A retrieval-augmented generation (RAG) based study assistant that answers questions grounded strictly in NCERT Class 9 Science content. 

Live Link : https://ncert-study-assistant-jreoqmevbx9rykyie7cthz.streamlit.app/
---

## What It Does

- Answers questions from NCERT Class 9 Science (Chapter 8 — Force and Laws of Motion)
- Retrieves relevant textbook chunks before generating any answer
- Refuses to answer when the answer is not found in the textbook
- Shows the source chunks used to generate the answer

---

## Architecture

```
User Question
     ↓
BM25 Retriever → searches 30 chunks from Chapter 8
     ↓
Top 3 relevant chunks retrieved
     ↓
Grounded Prompt → "Answer ONLY from context, refuse if not present"
     ↓
Groq LLM (Llama 3.1) → generates answer
     ↓
Answer + Source Chunks shown to user
```

---

## Project Structure

```
ncert-study-assistant/
│
├── data/
│   ├── raw/                  ← NCERT PDFs (not committed)
│   └── processed/
│       ├── extracted.json    ← cleaned text from PDF
│       └── chunks.json       ← 30 chunks with overlap
│
├── src/
│   ├── extract.py            ← PDF → clean text
│   ├── chunk.py              ← text → chunks (size=250, overlap=50)
│   ├── retriever.py          ← BM25 index + top-k retrieval
│   └── generator.py          ← grounded LLM prompt + Groq API
│
├── app.py                    ← Streamlit UI
├── evaluation_results.csv    ← 17-question evaluation results
├── requirements.txt
└── .env                      ← API keys (not committed)
```

---

## Stack

| Layer | Tool |
|---|---|
| PDF Extraction | PyMuPDF |
| Retrieval | BM25 (`rank_bm25`) |
| LLM | Groq API — Llama 3.1 8B |
| Interface | Streamlit |
| Deployment | Streamlit Community Cloud |

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

> Note: PDFs are not committed to this repo. Link to official NCERT source above.

**6. Run the pipeline**
```bash
# Extract and clean PDF
python src/extract.py

# Chunk the text
python src/chunk.py

# Run the app
python -m streamlit run app.py
```

---

## Evaluation Results Summary

Evaluated on 17 questions across three types:

| Type | Count | Correct | Wrong Refusals |
|---|---|---|---|
| Direct | 10 | 5 | 5 |
| Paraphrased | 3 | 3 | 0 |
| Out-of-scope | 4 | — | — |

**Out-of-scope refusal rate: 4/4 (100%)** 

**Key finding:** BM25 fails on momentum-related questions because the word "momentum" appears in context but the query words ("definition", "formula", "SI units") don't co-occur with it in the same chunks. This is BM25's core limitation — keyword matching without semantic understanding.

Full results: see `evaluation_results.csv`

---

## Known Limitations

- BM25 retrieval misses semantically related chunks when query vocabulary doesn't match chunk vocabulary exactly
- Only Chapter 8 (Force and Laws of Motion) is currently indexed
- Equations and special characters from PDF extraction may be inconsistent

---

## What's Next (Advanced Tier)

- Dense retrieval using `sentence-transformers` to fix momentum failures
- Add Chapter 9 to the index
- Compare BM25 vs dense retrieval on the same evaluation set
- Add explicit guardrails for out-of-scope and prompt injection

---

## Data Source

NCERT Class 9 Science Textbook - Official Source:
https://ncert.nic.in/textbook.php?iesc1=0-15

PDF files are not committed to this repository. Download directly from NCERT.