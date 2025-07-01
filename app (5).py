
import streamlit as st
import re
import tempfile
import spacy
import textstat
import pdfplumber
import docx
import openai

# Download SpaCy model if missing
try:
    nlp = spacy.load("en_core_web_sm")
except:
    import os
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

st.set_page_config(page_title="AI Resume Sculptor", layout="centered")

# Splash Logo
st.image("https://i.ibb.co/gJ1M5pL/logo-splash.png", use_column_width=True)
st.markdown("<h3 style='text-align: center;'>AI Resume Sculptor</h3>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# Resume Upload
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
        common_skills = ['python', 'java', 'sql', 'machine learning', 'data analysis', 'communication', 'leadership']
        return list({skill for skill in common_skills if skill in text.lower()})

    text = extract_text(filename)
    email = extract_email(text)
    name = extract_name(text)
    skills = extract_skills(text)

    st.subheader("📄 Extracted Info")
    st.write("👤 Name:", name)
    st.write("📧 Email:", email)
    st.write("🛠️ Skills:", ", ".join(skills))
    st.text_area("📝 Resume Text", text[:3000])

# AI Chatbot (LAKS)
st.subheader("🤖 Ask LAKS AI")
user_input = st.text_input("Type your question (e.g. job tips, company info):")
if user_input:
    openai.api_key = "your-openai-api-key"  # Replace with your actual key
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You're a helpful career advisor."},
                {"role": "user", "content": user_input}
            ]
        )
        st.success(response.choices[0].message["content"])
    except Exception as e:
        st.error("Error: " + str(e))

# Mock Interview
st.subheader("🎤 HR Mock Interview")
questions = [
    "Tell me about yourself.",
    "Why do you want to join our company?",
    "What are your strengths?",
    "Describe a project you’re proud of.",
    "Where do you see yourself in 5 years?"
]

for i, q in enumerate(questions):
    st.write(f"**Q{i+1}: {q}**")
    st.text_input(f"Your Answer (or speak if using voice tools)", key=f"answer_{i}")
    st.info("💡 Tip: Practice aloud or type your answer.")

st.success("✅ Mock interview recorded. Good luck!")

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("🔗 Powered by Streamlit + OpenAI", unsafe_allow_html=True)
