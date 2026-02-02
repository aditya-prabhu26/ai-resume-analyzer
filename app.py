import streamlit as st
import pdfplumber
from PIL import Image
import pytesseract
import re
import os
from dotenv import load_dotenv
from groq import Groq

# ---------- Load .env ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.error("❌ GROQ_API_KEY not found. Check .env file.")
    st.stop()

client = Groq(api_key=api_key)

# ---------- Page Config ----------
st.set_page_config(
    page_title="AI Resume Reviewer",
    page_icon="📄",
    layout="centered"
)

# ---------- Styling ----------
st.markdown("""
<style>
.header-box {
    background: #22c55e;
    padding: 22px;
    border-radius: 16px;
    margin-bottom: 25px;
}
.header-title {
    color: white;
    text-align: center;
    font-size: 34px;
    font-weight: 700;
}
.header-subtitle {
    color: #dcfce7;
    text-align: center;
    font-size: 16px;
}
.center-button button {
    width: 100%;
    background-color: #22c55e !important;
    color: white !important;
    border-radius: 10px !important;
    font-weight: 600;
    border: none !important;
}
</style>
""", unsafe_allow_html=True)

# ---------- Text Extraction ----------
def extract_text(file):
    if file.type == "application/pdf":
        with pdfplumber.open(file) as pdf:
            return "".join(page.extract_text() or "" for page in pdf.pages)
    else:
        image = Image.open(file)
        return pytesseract.image_to_string(image)

# ---------- ATS Scoring ----------
def calculate_scores(text):
    text_lower = text.lower()

    content = 95 if len(text) > 1200 else 80 if len(text) > 700 else 60

    contact = 50 if "@" in text else 0
    contact += 50 if re.search(r"\d{10}", text) else 0

    skills_keywords = ["python", "java", "sql", "html", "css", "machine learning", "data"]
    skills = min(60 + sum(k in text_lower for k in skills_keywords) * 5, 100)

    experience = 80 if "experience" in text_lower else 55

    projects = 95 if text_lower.count("project") >= 3 else 70

    overall = int((content + contact + skills + experience + projects) / 5)

    return content, contact, skills, experience, projects, overall

# ---------- ATS Bar ----------
def ats_bar(title, score):
    color = "#22c55e" if score >= 85 else "#f59e0b" if score >= 70 else "#ef4444"
    status = "No issues" if score >= 85 else "Minor issues" if score >= 70 else "Needs improvement"

    st.markdown(f"""
    <div style="margin-bottom:14px;">
        <div style="display:flex;justify-content:space-between;font-weight:600;">
            <span>{title}</span>
            <span style="color:{color};">{score}%</span>
        </div>
        <div style="background:#e5e7eb;border-radius:10px;height:10px;">
            <div style="width:{score}%;background:{color};height:10px;border-radius:10px;"></div>
        </div>
        <small style="color:{color};">{status}</small>
    </div>
    """, unsafe_allow_html=True)

# ---------- PROMPTS ----------
def review_prompt(resume_text, role):
    return f"""
You are a senior HR and ATS specialist.

Analyze the following resume for the role of: {role}

Resume Content:
{resume_text}

Provide:
1. Strengths
2. Weaknesses
3. Missing skills
4. Improvements
5. Final verdict
"""

def keyword_prompt(resume_text, role):
    return f"""
You are an ATS system.

For the role: {role}

From the resume below, list:
1. Keywords present
2. Important keywords missing

Resume:
{resume_text}
"""

# ---------- UI ----------
st.markdown("""
<div class="header-box">
    <div class="header-title">AI Resume Reviewer</div>
    <div class="header-subtitle">Upload your resume and get AI-powered feedback</div>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Upload Resume (PDF / JPG / PNG)",
    type=["pdf", "jpg", "jpeg", "png"]
)

job_role = st.selectbox(
    "Target Job Role",
    ["Software Engineer", "Data Analyst", "Data Scientist",
     "Web Developer", "AI / ML Engineer", "Intern / Fresher", "Other"]
)

analyze_clicked = st.button("🔍 Analyze Resume")

# ---------- Analysis ----------
if analyze_clicked:

    if not uploaded_file:
        st.error("Please upload a resume file.")
        st.stop()

    with st.spinner("Analyzing resume..."):
        resume_text = extract_text(uploaded_file)
        c, ct, sk, ex, pr, overall = calculate_scores(resume_text)

        review = review_prompt(resume_text, job_role)
        keywords = keyword_prompt(resume_text, job_role)

        response_review = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": review}],
            temperature=0.3
        )

        response_keywords = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": keywords}],
            temperature=0.3
        )

        ai_result = response_review.choices[0].message.content
        keyword_result = response_keywords.choices[0].message.content

    st.success("Resume analysis completed!")

    st.subheader("Overall ATS Score")
    st.markdown(f"## **{overall} / 100**")

    st.subheader("ATS Section Breakdown")
    ats_bar("Resume Content", c)
    ats_bar("Contact Information", ct)
    ats_bar("Skills", sk)
    ats_bar("Experience", ex)
    ats_bar("Projects", pr)

    st.subheader("AI Resume Review")
    st.write(ai_result)

    st.subheader("ATS Keyword Analysis")
    st.write(keyword_result)
