import streamlit as st
from groq import Groq
import pdfplumber
from PIL import Image
import pytesseract
import re


# Page configuration

st.set_page_config(
    page_title="AI Resume Reviewer",
    page_icon="📄",
    layout="centered"
)


#  Styling
st.markdown(
    """
    <style>
        body {
            background-color: #e6fdd8;
        }

        .main-container {
            background: #ffffff;
            padding: 30px;
            border-radius: 16px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.08);
        }

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
    """,
    unsafe_allow_html=True
)


# Groq API

GROQ_API_KEY = "YOUR_GROQ_API_KEY"
client = Groq(api_key=GROQ_API_KEY)


# Helper functions
# -------------------------
def get_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text


def get_text_from_image(file):
    image = Image.open(file)
    return pytesseract.image_to_string(image)


# -------- Genuine Section Scoring --------
def content_score(text):
    length = len(text)
    if length > 1200:
        return 95
    elif length > 800:
        return 85
    elif length > 500:
        return 75
    else:
        return 60


def contact_score(text):
    score = 0
    if "@" in text:
        score += 50
    if re.search(r"\d{10}", text):
        score += 50
    return score


def skills_score(text):
    keywords = ["python", "java", "sql", "html", "css", "machine learning", "data"]
    count = sum(1 for k in keywords if k in text.lower())
    return min(60 + count * 5, 100)


def experience_score(text):
    if "experience" not in text.lower():
        return 55
    years = re.findall(r"\d+\s+years", text.lower())
    return 70 + min(len(years) * 10, 30)


def projects_score(text):
    count = text.lower().count("project")
    if count >= 3:
        return 95
    elif count == 2:
        return 85
    elif count == 1:
        return 70
    else:
        return 55


def overall_ats_score(scores):
    return int(sum(scores) / len(scores))


def ats_bar(title, score):
    if score >= 85:
        color = "#22c55e"
        status = "No issues"
    elif score >= 70:
        color = "#f59e0b"
        status = "Minor issues"
    else:
        color = "#ef4444"
        status = "Needs improvement"

    st.markdown(
        f"""
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
        """,
        unsafe_allow_html=True
    )


def create_prompt(resume_text, role):
    return (
        f"You are an HR professional reviewing a resume for the role of {role}.\n\n"
        f"Resume:\n{resume_text}\n\n"
        "Give strengths, weaknesses, missing skills, improvements and final verdict."
    )


# UI
#....................
st.markdown(
    """
    <div class="header-box">
        <div class="header-title"> AI Resume Reviewer</div>
        <div class="header-subtitle">
            Upload your resume and get AI-powered feedback
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    " Upload Resume (PDF / JPG / PNG)",
    type=["pdf", "jpg", "jpeg", "png"]
)

job_role = st.selectbox(
    "Target Job Role",
    [
        "Software Engineer",
        "Data Analyst",
        "Data Scientist",
        "Web Developer",
        "AI / ML Engineer",
        "Intern / Fresher",
        "Other"
    ]
)

st.markdown("<div class='center-button'>", unsafe_allow_html=True)
analyze_clicked = st.button("🔍 Analyze Resume")
st.markdown("</div>", unsafe_allow_html=True)


# file if not found

if analyze_clicked and not uploaded_file:
    st.error(" Please upload a resume file before analyzing.")


# Analysis

elif analyze_clicked and uploaded_file:
    with st.spinner("Analyzing resume..."):
        resume_text = (
            get_text_from_pdf(uploaded_file)
            if uploaded_file.type == "application/pdf"
            else get_text_from_image(uploaded_file)
        )

        c = content_score(resume_text)
        ct = contact_score(resume_text)
        sk = skills_score(resume_text)
        ex = experience_score(resume_text)
        pr = projects_score(resume_text)

        overall_score = overall_ats_score([c, ct, sk, ex, pr])

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": create_prompt(resume_text, job_role)}],
            temperature=0.3
        )

        ai_result = response.choices[0].message.content

    st.success("Resume analysis completed!")

    st.subheader(" Overall ATS Score")
    st.markdown(f"## **{overall_score} / 100**")

    st.subheader(" ATS Section Breakdown")
    ats_bar("Resume Content", c)
    ats_bar("Contact Information", ct)
    ats_bar("Skills", sk)
    ats_bar("Experience", ex)
    ats_bar("Projects", pr)

    st.subheader(" AI Resume Review")
    st.write(ai_result)

st.markdown("</div>", unsafe_allow_html=True)
