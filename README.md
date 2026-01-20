# 📄 AI Resume Reviewer

## 📌 About the Project
.... The AI Resume Reviewer is a web-based application that analyzes resumes and provides ATS-style evaluation using Artificial Intelligence.

.... The application is built using Streamlit for the user interface and Groq API for AI-powered resume analysis. It helps users understand how well their resume matches common Applicant Tracking System (ATS) requirements and suggests improvements.

#### ..... The main aim of this project is to help students and job seekers understand:

    . How strong their resume is

    . Which sections need improvement

    . How ATS systems generally evaluate resumes


## ⚙️ What the Application Does

    . Allows the user to upload a resume in PDF or image format

    . Extracts text automatically from the uploaded resume

    . Calculates an ATS score out of 100 based on resume content

#### .... Shows section-wise ATS analysis:

  . Resume content

  . Contact information

  . Skills

  . Experience

  . Projects

#### ..... Displays the status of each section as:

  . No issues

  . Minor issues

  . Needs improvement

  . Uses AI to generate detailed feedback such as:

  . Strengths of the resume

  . Weaknesses

  . Missing skills or sections

  . Suggestions for improvement

  . Final verdict

## 🛠 Technologies Used

    . Python – main programming language

    . Streamlit – for building the web interface

    . Groq API (LLaMA 3.1) – for AI-based resume feedback

    . pdfplumber – to extract text from PDF resumes

    . pytesseract & Pillow – to extract text from image resumes

## 📂 Project Structure

AI-Resume-Reviewer/
│
├── app.py        # Main  file
├── README.md     # Project documentation

## ▶️ How to Run the Project

  ### 1️⃣ Install Python

      Make sure Python (version 3.9 or above) is installed on your system.

      Check version:

          python --version

  ### 2️⃣ Create a Virtual Environment (Optional)

          python -m venv venv

      Activate it:

          venv\Scripts\activate

  ### 3️⃣ Install Required Libraries

          pip install streamlit groq pdfplumber pillow pytesseract

  ### 4️⃣ Install Tesseract OCR

      This is required for reading text from image resumes.

          Download from:
          https://github.com/UB-Mannheim/tesseract/wik

   ### 5️⃣ Add Groq API Key

      In app.py and replace the API key placeholder:

          GROQ_API_KEY = "YOUR_GROQ_API_KEY"

  ### 6️⃣ Run the Application
          
          streamlit run app.py

## 🧪 How to Use the Application

  . Upload your resume (PDF / JPG / PNG)

  . Select the target job role

  . Click Analyze Resume

   # View:

      . ATS score

      . Section-wise analysis

      . AI-generated resume feedback

## ⚠️ Limitations

  . ATS score is an approximation, not an official ATS result

  . Accuracy depends on resume clarity and formatting

  . Image resumes work best when text is clear

## 🚀 Future Enhancements

  . Resume vs Job Description matching

  . Download ATS report as PDF

  . Keyword optimization suggestions

  . Improved resume scoring logic

## ✅ Conclusion

This project shows how AI can be used to analyze resumes and give meaningful feedback.

