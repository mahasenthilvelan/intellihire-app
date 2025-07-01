
import streamlit as st
import re
import tempfile

try:
    import spacy
except ImportError:
    import os
    os.system("pip install spacy")
    import spacy

try:
    import pdfplumber
except ImportError:
    import os
    os.system("pip install pdfplumber")
    import pdfplumber

import docx
import textstat

# Load NLP model
try:
    nlp = spacy.load("en_core_web_sm")
except:
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

st.set_page_config(page_title="AI Resume Sculptor", layout="centered")
st.title("🎯 AI Resume Sculptor")

# Upload Resume
uploaded_file = st.file_uploader("📁 Upload your resume (PDF or DOCX)", type=["pdf", "docx"], key="resume_upload")

def extract_text(file_path):
    if file_path.endswith(".pdf"):
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text
    elif file_path.endswith(".docx"):
        doc = docx.Document(file_path)
        return "\n".join([p.text for p in doc.paragraphs])
    return ""

def extract_email(text):
    match = re.search(r"[\w.-]+@[\w.-]+", text)
    return match.group(0) if match else "Not found"

def extract_phone(text):
    match = re.search(r"\+?\d[\d\s\-]{8,}", text)
    return match.group(0) if match else "Not found"

def extract_skills(text):
    common_skills = ['python', 'java', 'sql', 'machine learning', 'data analysis', 'communication', 'leadership']
    doc = nlp(text.lower())
    return list(set([token.text for token in doc if token.text in common_skills]))

def soft_signal_analysis(text):
    return {
        "Readability Score": round(textstat.flesch_reading_ease(text), 2),
        "Avg Sentence Length": round(textstat.avg_sentence_length(text), 2),
        "Word Count": len(text.split())
    }

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=uploaded_file.name[-5:]) as tmp:
        tmp.write(uploaded_file.read())
        path = tmp.name

    resume_text = extract_text(path)
    email = extract_email(resume_text)
    phone = extract_phone(resume_text)
    skills = extract_skills(resume_text)
    soft_signals = soft_signal_analysis(resume_text)

    st.subheader("📄 Resume Summary")
    st.write("📧 Email:", email)
    st.write("📞 Phone:", phone)
    st.write("🧠 Skills:", ", ".join(skills))
    st.write("📝 Soft Signal Analysis")
    for key, val in soft_signals.items():
        st.write(f"{key}: {val}")
    st.text_area("📜 Resume Preview", resume_text[:3000])
else:
    st.info("Upload your resume to analyze.")
