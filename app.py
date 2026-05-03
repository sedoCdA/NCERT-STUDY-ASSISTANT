import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from src.generator import answer

# Page config
st.set_page_config(page_title="NCERT Study Assistant", page_icon="📚")

# Title
st.title("📚 NCERT Class 9 Science Assistant")
st.caption("Chapter 8 - Force and Laws of Motion · Answers grounded in NCERT content")

# Input
question = st.text_input("Ask a question:", 
                          placeholder="e.g. What is Newton's First Law?")

if st.button("Ask") and question:
    with st.spinner("Searching textbook..."):
        result = answer(question, use_dense=True, strict=True)

    # Show answer
    st.subheader("Answer")
    st.write(result["answer"])

    # Show retrieved chunks
    with st.expander("📄 Source chunks used"):
        for chunk in result["chunks"]:
            st.markdown(f"**Chunk {chunk['chunk_id']}** — `{chunk.get('content_type', 'prose')}`")
            st.caption(chunk["text"][:400])
            st.divider()