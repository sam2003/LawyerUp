import streamlit as st
import os
from utils import extract_text_from_pdf, suggest_clause_improvements



st.title("💡 Clause Improvement Suggestions")
st.write("Upload a PDF file to analyze missing or weak clauses and receive suggestions for improvement.")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"], key="suggestions_upload")

if uploaded_file is not None:
    UPLOAD_FOLDER = "uploads"
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
    
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    text = extract_text_from_pdf(file_path)
    os.remove(file_path)
    
    st.write("📂 **File Uploaded Successfully:**", uploaded_file.name)
    
    with st.spinner("💡 Analyzing clause improvements..."):
        suggestions = suggest_clause_improvements(text)
    
    st.subheader("💡 Suggested Clause Improvements")
    st.write(suggestions)
