import streamlit as st
import time
import pdfplumber
import docx2txt
import re
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ✅ Load SpaCy model safely
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    st.error("SpaCy model not found. Please run: python -m spacy download en_core_web_sm")
    st.stop()

# ✅ Use session state
if 'page' not in st.session_state:
    st.session_state['page'] = 'splash'
    st.session_state['splash_done'] = False

# ✅ Splash
if st.session_state['page'] == 'splash':
    if not st.session_state['splash_done']:
        st.image('logo.png', width=200)
        st.title("Welcome to IntelliHire")
        time.sleep(1)
        st.session_state['splash_done'] = True
        st.session_state['page'] = 'login'
        st.stop()
    else:
        st.session_state['page'] = 'login'

# ✅ Login
if st.session_state['page'] == 'login':
    st.header("🔐 Login")
    option = st.radio("Login with", ["Email/Password", "Google"])
    if option == "Email/Password":
        u = st.text_input("Username")
        e = st.text_input("Email")
        p = st.text_input("Password", type="password")
        if st.button("Login"):
            if u and e and p:
                st.session_state['page'] = 'profile'
                st.stop()
    else:
        if st.button("Google Login"):
            st.session_state['page'] = 'profile'
            st.stop()

# ✅ Profile
if st.session_state['page'] == 'profile':
    st.header("👤 Profile")
    with st.form("profile_form"):
        st.text_input("Name")
        st.date_input("DOB")
        st.radio("Gender", ["Male", "Female", "Other"])
        st.text_input("Email")
        st.text_area("Permanent Address")
        st.text_area("Temporary Address")
        st.text_input("City")
        st.text_input("State")
        st.text_input("Phone")
        st.text_input("Qualification")
        st.text_input("Mother Tongue")
        st.text_input("Languages Known")
        if st.form_submit_button("Save"):
            st.session_state['page'] = 'company'
            st.stop()

# ✅ Company
if st.session_state['page'] == 'company':
    st.header("🏢 Company Registration")
    with st.form("company_form"):
        st.text_input("Company Name")
        st.text_input("Location")
        st.text_input("Branch")
        st.text_area("Type")
        if st.form_submit_button("Register"):
            st.session_state['page'] = 'dashboard'
            st.stop()

# ✅ Dashboard
if st.session_state['page'] == 'dashboard':
    st.header("📂 Dashboard")
    up = st.file_uploader("Upload Resume", type=["pdf", "docx"])
    if up:
        def extract(f):
            return (
                docx2txt.process(f)
                if f.name.endswith("docx")
                else "".join([p.extract_text() for p in pdfplumber.open(f).pages])
            )

        text = extract(up)
        st.write(text[:300])

        doc = nlp(text)
        ent_name = next((e.text for e in doc.ents if e.label_ == "PERSON"), "None")
        st.write(f"Name: {ent_name}")

        tfidf = TfidfVectorizer()
        res = tfidf.fit_transform([text, "python java sql"])
        sim = cosine_similarity(res[0:1], res[1:2])[0][0]
        st.write(f"TF-IDF: {round(sim * 100, 2)}% match")

    st.button("Soft Signal Analyzer")
    st.button("HR Q&A")
    st.button("Mock Interview")
    st.button("Scheduler")
    st.button("Feedback")
    st.button("Kannama Chatbot")
