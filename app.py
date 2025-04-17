import streamlit as st
import os
import base64
from io import BytesIO
from PIL import Image
from utils import extract_text_from_pdf
import streamlit.components.v1 as components
st.set_page_config(
    page_title="SAMS Legal Document Analyzer",
    page_icon="LOGO.png",
    layout="wide",
)
st.markdown("""
    <head>
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5876158560001890"
     crossorigin="anonymous"></script>
    </head>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
    /* Force main content to a fixed width and align left */
    .main .block-container {
        max-width: 1000px;      /* Fixed width for content */
        margin-left: 2rem !important;
        margin-right: 350px !important;
        padding-right: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
        MainMenu {visibility: hidden;}
        header {visibility: hidden;}
    </style>""", unsafe_allow_html=True
)

left_col, right_col = st.columns([3, 1])
with left_col:
    # Initialize session state for navigation
    if "current_page" not in st.session_state:
        st.session_state.current_page = "home"

    # Function to convert image to Base64
    def image_to_base64(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()

    logo_base64 = image_to_base64("LOGO.png")

    # Sidebar with Logo and Title
    with st.sidebar:
        col1, col2 = st.columns([1, 3])  # Adjust width ratio

        with col1:
            st.markdown(
                
                f"""
                <a href='/' style='text-decoration: none;' target='_self'>
                    <img src="data:image/png;base64,{logo_base64}" width="50">
                </a>
                """,
                unsafe_allow_html=True
            )

        with col2:
            st.title("SAMS LDA")

    # Manual Navigation
    st.sidebar.header("Navigation")
    if st.sidebar.button("🏠 Home"):
        st.session_state.current_page = "home"
    if st.sidebar.button("📄 Summarize"):
        st.session_state.current_page = "1_Summarize"
    if st.sidebar.button("🔍 Extract Clauses"):
        st.session_state.current_page = "2_Extract_Clauses"
    if st.sidebar.button("🔄 Compare Contracts"):
        st.session_state.current_page = "3_Compare_Contracts"
    if st.sidebar.button("💡 Clause Suggestions"):
        st.session_state.current_page = "4_Clause_Suggestions"
    if st.sidebar.button("📝 AI Contract Drafting"):
        st.session_state.current_page = "5_AI_Contract_Drafting"

    # Footer Disclaimer


    # Load the selected module dynamically with UTF-8 encoding
    if st.session_state.current_page == "home":
        
        col1, col2 = st.columns([1, 6])
        with col1:
            st.image("LOGO.png", width=200)
        with col2:
            st.title("Welcome to the Lawyered")
        st.info("Please select a functionality from the sidebar.")
        ad_code = """
        <head>
            <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5876158560001890"
                crossorigin="anonymous"></script>
        </head>
        """

        components.html(ad_code, height=250)
    else:
        module_path = f"modules/{st.session_state.current_page}.py"
        if os.path.exists(module_path):
            with open(module_path, "r", encoding="utf-8") as file:
                exec(file.read())  # Execute the module safely
        else:
            st.error(f"Error: {module_path} not found!")


# with right_col:
st.markdown("""
    <style>
    .floating-ad {
        position: fixed;
        top: 100px;
        right: 20px;
        width: 300px;
        height: 600px;
        z-index: 100;
        box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
        border-radius: 8px;
        background: white;
    }
    </style>
    <div class="floating-ad">
        <iframe src="http://adpage.rf.gd/" width="300" height="600" frameborder="0" scrolling="no"></iframe>
    </div>
""", unsafe_allow_html=True)

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
