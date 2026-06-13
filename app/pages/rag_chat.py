import streamlit as st

st.title("🧠 Supply Chain RAG Chatbot")

question = st.text_input("Ask a question")

if question:
    st.write("You asked:", question)