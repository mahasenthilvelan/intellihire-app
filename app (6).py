
import streamlit as st
import re
import tempfile
import pdfplumber
import docx
import textstat
import subprocess

# --- Load spacy model with fallback ---
import spacy
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

st.set_page_config(page_title="AI Resume Sculptor", layout="centered")

# Step 0: Logo/Splash
st.image("https://i.ibb.co/gJ1M5pL/logo-splash.png", use_column_width=True)
st.markdown("<h3 style='text-align: center;'>AI Resume Sculptor</h3>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# Step 1: Login UI (simplified)
with st.expander("🔐 Login to continue"):
    login_method = st.radio("Choose login method", ["Email/Password", "Google (Simulated)"], horizontal=True)
    if login_method == "Email/Password":
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            st.success(f"Welcome {email}")
    elif login_method == "Google (Simulated)":
        if st.button("Continue with Google"):
            st.success("Simulated Google Login Successful")

# Step 2: Upload Resume
uploaded_file = st.file_uploader("📁 Upload Resume", type=["pdf", "docx"], key="resume_uploader")
if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.read())
        filename = tmp_file.name

    def extract_text(fname):
        if fname.endswith(".pdf"):
            with pdfplumber.open(fname) as pdf:
                return "\n".join([p.extract_text() or "" for p in pdf.pages])
        elif fname.endswith(".docx"):
            return "\n".join([para.text for para in docx.Document(fname).paragraphs])
        return ""

    def extract_email(text):
        match = re.search(r"[\w.-]+@[\w.-]+", text)
        return match.group(0) if match else "Not Found"

    def extract_name(text):
        doc = nlp(text)
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                return ent.text
        return "Not Found"

    def extract_skills(text):
        keywords = ['python', 'sql', 'java', 'machine learning', 'data analysis', 'communication', 'leadership']
        return [word for word in keywords if word in text.lower()]

    text = extract_text(filename)
    email = extract_email(text)
    name = extract_name(text)
    skills = extract_skills(text)

    st.subheader("📄 Extracted Info")
    st.write("🧑 Name:", name)
    st.write("📧 Email:", email)
    st.write("💼 Skills:", ", ".join(skills))
    st.text_area("📝 Resume Text", text[:3000])
