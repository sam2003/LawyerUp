import streamlit as st
import os
from utils import extract_text_from_pdf, analyze_contract



st.title("🔍 Extract Legal Clauses")
st.write("Upload a legal document to extract and classify its clauses.")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"], key="clauses_upload")

if uploaded_file is not None:
    UPLOAD_FOLDER = "uploads"
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    text = extract_text_from_pdf(file_path)
    os.remove(file_path)  # Delete after processing
    
    st.write("📂 **File Uploaded Successfully:**", uploaded_file.name)
    
    with st.spinner("🔍 Extracting legal clauses..."):
        clauses = analyze_contract(text)
    
    st.subheader("🔍 Extracted Legal Clauses")
    
    if "error" in clauses:
        st.error(clauses["error"])
    else:
        for clause, content in clauses.items():
            if isinstance(content, list):  # Convert list to string
                content = "\n".join(content)
            if content.strip():
                with st.expander(f"📌 {clause}"):
                    st.write(content)
    
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
