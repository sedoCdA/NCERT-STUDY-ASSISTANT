import streamlit as st
from src.generator import answer

# Page config
st.set_page_config(page_title="NCERT Study Assistant", page_icon="📚")

# Title
st.title("📚 NCERT Class 9 Science Assistant")
st.caption("Answers grounded in Chapter 8 — Force and Laws of Motion")

# Input
question = st.text_input("Ask a question from Chapter 8:", 
                          placeholder="e.g. What is Newton's First Law?")

if st.button("Ask") and question:
    with st.spinner("Searching textbook..."):
        result = answer(question)
    
    # Show answer
    st.subheader("Answer")
    st.write(result["answer"])
    
    # Show retrieved chunks
    with st.expander("📄 Source chunks used"):
        for i, chunk in enumerate(result["chunks"]):
            st.markdown(f"**Chunk {chunk['chunk_id']}**")
            st.caption(chunk["text"][:400])
            st.divider()