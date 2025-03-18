import streamlit as st
import os
import requests
import fitz  # PyMuPDF for PDF text extraction
import easyocr  # EasyOCR for scanned PDFs
import json

st.set_page_config(
    page_title="SAMS Legal Document Analyzer",
    page_icon="LOGO.png",
    layout="centered",
)

# 🔹 Replace with your actual Google Gemini API Key
GEMINI_API_KEY = "AIzaSyDRGyt_pU3i-uLfeI5hXZhw4qHDTbTThVc"

# Google Gemini API URL
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

# Ensure "uploads" directory exists
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text += page.get_text("text") + "\n"

        if not text.strip():
            images = [page.get_pixmap() for page in doc]
            for img in images:
                text += " ".join(reader.readtext(img.tobytes(), detail=0)) + "\n"
    except Exception as e:
        return f"Error extracting text: {str(e)}"

    return text.strip() if text.strip() else "No text found in the PDF."

# Function to analyze contract clauses
def analyze_contract(text):
    prompt = f"""
    Extract and classify legal clauses from the following contract text.
    Categorize them into:
    - Termination Clause
    - Liability Clause
    - Confidentiality Clause
    - Payment Clause
    - Jurisdiction Clause
    - Force Majeure
    - Dispute Resolution
    - Non-Compete Agreement

    Return a structured JSON output with extracted clauses.
    Contract Text:
    {text}
    """
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    response = requests.post(GEMINI_API_URL, json=payload)
    result = response.json()

    if "error" in result:
        return {"error": f"API Error: {result['error']['message']}"}

    try:
        raw_output = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
        raw_output = raw_output.strip().replace("```json", "").replace("```", "").strip()
        clauses_json = json.loads(raw_output)
    except json.JSONDecodeError:
        clauses_json = {"error": "Failed to parse JSON output from API"}

    return clauses_json

# Function to summarize contract text
def summarize_contract(text):
    prompt = f"""
    Summarize the following legal contract in 300 words or less. Focus on key terms, obligations, and important clauses.

    Contract Text:
    {text}
    """
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    response = requests.post(GEMINI_API_URL, json=payload)
    result = response.json()

    if "error" in result:
        return {"error": f"Summarization error: {result['error']['message']}"}

    try:
        raw_output = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
    except KeyError:
        raw_output = "Summarization failed"

    return raw_output

# Function to compare two contracts using AI
def compare_contracts(text1, text2):
    prompt = f"""
    Compare the following two legal contracts and highlight the differences in their clauses, obligations, and key terms.
    
    Contract 1:
    {text1}
    
    Contract 2:
    {text2}
    
    Provide a structured comparison, showing the differences in each clause or term.
    """
    
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    response = requests.post(GEMINI_API_URL, json=payload)
    result = response.json()

    if "error" in result:
        return {"error": f"API Error: {result['error']['message']}"}

    try:
        raw_output = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
    except KeyError:
        raw_output = "Comparison failed"

    return raw_output

def suggest_clause_improvements(text):
    prompt = f"""
    Analyze the following contract text and provide suggestions for improving weak or missing clauses.
    
    Contract Text:
    {text}
    """
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    response = requests.post(GEMINI_API_URL, json=payload)
    result = response.json()

    if "error" in result:
        return {"error": f"API Error: {result['error']['message']}"}

    try:
        suggestions = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
    except KeyError:
        suggestions = "No suggestions available"

    return suggestions

col1, col2 = st.columns([1,7])

with col1:
    st.image("LOGO.png")
with col2:
    st.title("SAMS : Legal Doc Analyzer")

# **Tabs for different functionalities**
tab1, tab2, tab3, tab4 = st.tabs(["📄 Summarize", "🔍 Extract Clauses", "🔄 Compare Contracts", "💡 Clause Suggestions"])

with tab1:  # **Summarization Tab**
    st.header("Summarize Legal Document")
    uploaded_file = st.file_uploader("Upload a PDF file for summarization", type=["pdf"], key="summarize_upload")

    if uploaded_file is not None:
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)

        # Save the uploaded file
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        text = extract_text_from_pdf(file_path)
        os.remove(file_path)  # Delete after processing

        st.write("📂 **File Uploaded Successfully:**", uploaded_file.name)

        with st.spinner("📄 Summarizing document..."):
            summary = summarize_contract(text)

        st.subheader("📄 Document Summary")
        st.write(summary)

with tab2:  # **Clause Extraction Tab**
    st.header("Extract Legal Clauses")
    uploaded_file = st.file_uploader("Upload a PDF file for clause extraction", type=["pdf"], key="clauses_upload")

    if uploaded_file is not None:
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)

        # Save the uploaded file
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

with tab3:
    st.header("Compare Two Contracts")
    uploaded_file1 = st.file_uploader("Upload First Contract", type=["pdf"], key="compare_upload1")
    uploaded_file2 = st.file_uploader("Upload Second Contract", type=["pdf"], key="compare_upload2")

    if uploaded_file1 and uploaded_file2:
        file_path1 = os.path.join(UPLOAD_FOLDER, uploaded_file1.name)
        file_path2 = os.path.join(UPLOAD_FOLDER, uploaded_file2.name)

        # Save both files
        with open(file_path1, "wb") as f:
            f.write(uploaded_file1.getbuffer())
        with open(file_path2, "wb") as f:
            f.write(uploaded_file2.getbuffer())

        text1 = extract_text_from_pdf(file_path1)
        text2 = extract_text_from_pdf(file_path2)

        os.remove(file_path1)
        os.remove(file_path2)

        st.write("📂 **Files Uploaded Successfully:**", uploaded_file1.name, " & ", uploaded_file2.name)

        with st.spinner("🔄 Comparing contracts..."):
            comparison_result = compare_contracts(text1, text2)

        st.subheader("🔄 Contract Comparison")
        st.write(comparison_result)

with tab4:  # **Clause Improvement Suggestions Tab**
    st.header("Clause Improvement Suggestions")
    uploaded_file = st.file_uploader("Upload a PDF file to analyze missing or weak clauses", type=["pdf"], key="suggestions_upload")

    if uploaded_file is not None:
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)

        # Save the uploaded file
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        text = extract_text_from_pdf(file_path)
        os.remove(file_path)  # Delete after processing

        st.write("📂 **File Uploaded Successfully:**", uploaded_file.name)

        with st.spinner("💡 Analyzing clause improvements..."):
            suggestions = suggest_clause_improvements(text)

        st.subheader("💡 Suggested Clause Improvements")
        st.write(suggestions)
# 🚀 Footer
st.markdown("""
    <style>
        /* Ensure footer remains at the bottom and adapts to sidebar */
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #f1f1f1;
            text-align: center;
            padding: 10px;
            font-size: 14px;
            color: #333;
            z-index: 9999;
            transition: margin-left 0.3s ease-in-out; /* Smooth transition */
        }

        /* Adjust footer margin when sidebar is present */
        .sidebar-open .footer {
            margin-left: 300px; /* Adjust based on sidebar width */
            width: calc(100% - 300px); /* Keep footer centered when sidebar is there */
        }

        /* Add padding to prevent content from being hidden under footer */
        .main-content {
            padding-bottom: 60px;
        }

        /* Adjust sidebar width */
        section[data-testid="stSidebar"] {
            width: 300px !important;
        }

        /* Detect sidebar presence and apply class */
        body:has(section[data-testid="stSidebar"]) .footer {
            margin-left: 300px;
            width: calc(100% - 300px);
        }

    </style>
    <div class="footer">
        🚨 This AI tool provides informational analysis only and does not constitute legal advice; please consult a qualified lawyer for legal matters.
        Developed by <b>SAMS</b> | © 2025 All Rights Reserved
    </div>
""", unsafe_allow_html=True)

# Add a spacer to push content above the footer
st.write("<div class='main-content'></div>", unsafe_allow_html=True)
