import streamlit as st
import os
from utils import extract_text_from_pdf, draft_contract

st.title("✍️ AI-Powered Contract Drafting")
st.write("Generate a legal document based on your input.")

# Contract Type Selection
contract_types = ["Employment Agreement", "Non-Disclosure Agreement (NDA)", "Service Agreement", "Lease Agreement", "Partnership Agreement", "Other"]
selected_contract = st.selectbox("Select Contract Type", contract_types, key="contract_type")

# If "Other" is selected, show a text input for custom contract type
custom_contract_type = ""
if selected_contract == "Other":
    custom_contract_type = st.text_input("Enter Contract Type", key="custom_contract")

# Party Names and Effective Date
party_one = st.text_input("Enter First Party Name", key="party_one")
party_two = st.text_input("Enter Second Party Name", key="party_two")
effective_date = st.date_input("Effective Date", key="effective_date")

# Key Terms
key_terms = st.text_area("Enter Key Terms and Conditions", key="key_terms")

# Optional: Contract Description
contract_description = st.text_area("Provide Additional Description (Optional)", key="contract_description")

# Option to upload an existing contract for modification
uploaded_contract = st.file_uploader("Upload an Existing Contract (Optional)", type=["pdf"], key="existing_contract_upload")

existing_contract_text = ""
if uploaded_contract:
    UPLOAD_FOLDER = "uploads"
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    file_path = os.path.join(UPLOAD_FOLDER, uploaded_contract.name)

    # Save and extract text
    with open(file_path, "wb") as f:
        f.write(uploaded_contract.getbuffer())

    existing_contract_text = extract_text_from_pdf(file_path)
    os.remove(file_path)  # Clean up after processing

    st.write("📂 **Existing Contract Uploaded Successfully:**", uploaded_contract.name)

# Generate Contract Button
if st.button("📝 Generate Contract"):
    st.write("⏳ **Generating contract... Please wait.**")

    # Determine the final contract type (selected or custom)
    final_contract_type = custom_contract_type if selected_contract == "Other" else selected_contract

    # Generate the contract
    generated_contract = draft_contract(final_contract_type, party_one, party_two, effective_date, key_terms, contract_description, existing_contract_text)

    # Display Result
    st.subheader("📄 Generated Contract")
    st.write(generated_contract)
