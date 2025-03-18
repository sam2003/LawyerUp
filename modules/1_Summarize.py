import streamlit as st
import os
from utils import extract_text_from_pdf, summarize_contract


st.title("📄 Summarize Legal Document")

uploaded_file = st.file_uploader("Upload a PDF file for summarization", type=["pdf"], key="summarize_upload")

if uploaded_file is not None:
    UPLOAD_FOLDER = "uploads"
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    text = extract_text_from_pdf(file_path)
    os.remove(file_path)

    st.write("📂 **File Uploaded Successfully:**", uploaded_file.name)

    with st.spinner("📄 Summarizing document..."):
        summary = summarize_contract(text)

    st.subheader("📄 Document Summary")
    st.write(summary)
