import os
import fitz  # PyMuPDF for PDF text extraction
import easyocr  # EasyOCR for scanned PDFs
import requests
import json

# Google Gemini API Key and URL
GEMINI_API_KEY = "AIzaSyDRGyt_pU3i-uLfeI5hXZhw4qHDTbTThVc"
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

# Ensure "uploads" directory exists
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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
        # Extract text response
        raw_output = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "").strip()
        
        # Debug: Print raw API response
        print("🛠 RAW OUTPUT FROM API:")
        print(raw_output)

        # Ensure it's valid JSON before parsing
        raw_output = raw_output.replace("```json", "").replace("```", "").strip()
        clauses_json = json.loads(raw_output)  # Convert to dict

        # Ensure values are always strings
        for clause, content in clauses_json.items():
            if isinstance(content, list):  # If list, join into a single string
                clauses_json[clause] = "\n".join([str(item) if isinstance(item, str) else json.dumps(item) for item in content])
            elif isinstance(content, dict):  # If dict, convert to JSON string
                clauses_json[clause] = json.dumps(content, indent=2)
        
    except json.JSONDecodeError as e:
        clauses_json = {"error": f"JSON Parsing Error: {str(e)}", "raw_response": raw_output}

    return clauses_json

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

def draft_contract(contract_type, party_one, party_two, effective_date, key_terms, description="", existing_contract_text=""):
    """
    Generate a legal contract based on user input.

    Parameters:
        contract_type (str): Type of contract (Employment, NDA, etc.).
        party_one (str): Name of the first party.
        party_two (str): Name of the second party.
        effective_date (str): Contract start date.
        key_terms (str): Important terms and conditions.
        description (str, optional): Additional description of the contract.
        existing_contract_text (str, optional): Existing contract text to modify.

    Returns:
        str: Generated contract text.
    """

    # Construct the prompt
    prompt = f"""
    Generate a professional legal contract.
    
    Contract Type: {contract_type}
    First Party: {party_one}
    Second Party: {party_two}
    Effective Date: {effective_date}
    Key Terms: {key_terms}
    
    Additional Description: {description}
    
    {"Modify the following existing contract instead of generating from scratch:" + existing_contract_text if existing_contract_text else ""}
    
    Ensure the contract is legally structured with appropriate clauses.
    """

    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    response = requests.post(GEMINI_API_URL, json=payload)
    result = response.json()

    if "error" in result:
        return f"API Error: {result['error']['message']}"

    try:
        generated_contract = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
    except KeyError:
        generated_contract = "Error generating contract."

    return generated_contract

