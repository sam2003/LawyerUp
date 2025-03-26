import streamlit as st
import os
from utils import extract_text_from_pdf, compare_contracts



st.title("🔄 Compare Contracts")

st.write("Upload two contract PDFs to compare their clauses and key terms.")

# File uploaders for two contracts
uploaded_file1 = st.file_uploader("Upload First Contract", type=["pdf"], key="compare_upload1")
uploaded_file2 = st.file_uploader("Upload Second Contract", type=["pdf"], key="compare_upload2")

if uploaded_file1 and uploaded_file2:
    file_path1 = os.path.join("uploads", uploaded_file1.name)
    file_path2 = os.path.join("uploads", uploaded_file2.name)

    # Save the uploaded files
    with open(file_path1, "wb") as f:
        f.write(uploaded_file1.getbuffer())
    with open(file_path2, "wb") as f:
        f.write(uploaded_file2.getbuffer())

    # Extract text from PDFs
    text1 = extract_text_from_pdf(file_path1)
    text2 = extract_text_from_pdf(file_path2)

    os.remove(file_path1)  # Clean up after extraction
    os.remove(file_path2)

    st.write("📂 **Files Uploaded Successfully:**", uploaded_file1.name, "&", uploaded_file2.name)

    with st.spinner("🔄 Comparing contracts..."):
        comparison_result = compare_contracts(text1, text2)

    st.subheader("🔍 Contract Comparison")
    st.write(comparison_result)
    ad_code = """
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5876158560001890"
         crossorigin="anonymous"></script>
    <ins class="adsbygoogle"
         style="display:block; text-align:center;"
         data-ad-layout="in-article"
         data-ad-format="fluid"
         data-ad-client="ca-pub-5876158560001890"
         data-ad-slot="6647795675"></ins>
    <script>
         (adsbygoogle = window.adsbygoogle || []).push({});
    </script>
    """
    
    st.components.v1.html(ad_code, height=300)
