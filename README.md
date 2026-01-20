AI Resume Reviewer
About the Project

The AI Resume Reviewer is a simple web application that analyzes resumes and gives feedback similar to an ATS (Applicant Tracking System).

The main aim of this project is to help students and job seekers understand:

How strong their resume is

Which sections need improvement

How ATS systems generally evaluate resumes

This project is built as a mini AI application using Streamlit and Groq API and is suitable for internship or academic submission.

What the Application Does

Allows the user to upload a resume in PDF or image format

Extracts text automatically from the uploaded resume

Calculates an ATS score out of 100 based on resume content

Shows section-wise ATS analysis:

Resume content

Contact information

Skills

Experience

Projects

Displays the status of each section as:

No issues

Minor issues

Needs improvement

Uses AI to generate detailed feedback such as:

Strengths of the resume

Weaknesses

Missing skills or sections

Suggestions for improvement

Final verdict

Technologies Used

Python – main programming language

Streamlit – for building the web interface

Groq API (LLaMA 3.1) – for AI-based resume feedback

pdfplumber – to extract text from PDF resumes

pytesseract & Pillow – to extract text from image resumes

Project Structure
AI-Resume-Reviewer/
│
├── app.py        # Main application file
├── README.md     # Project documentation

How the ATS Score Works

The ATS score is calculated based on real resume factors such as:

Presence of contact details (email and phone number)

Skills section availability

Experience details

Project information

Overall resume length and content quality

The score is not fixed and changes based on the resume uploaded.

How to Run the Project
Step 1: Install Python

Make sure Python (version 3.9 or above) is installed on your system.

Check version:

python --version

Step 2: Create a Virtual Environment (Optional)
python -m venv venv


Activate it:

Windows

venv\Scripts\activate


Mac / Linux

source venv/bin/activate

Step 3: Install Required Libraries
pip install streamlit groq pdfplumber pillow pytesseract

Step 4: Install Tesseract OCR

This is required for reading text from image resumes.

Windows:
Download from:
https://github.com/UB-Mannheim/tesseract/wiki

Linux:

sudo apt install tesseract-ocr


Mac:

brew install tesseract

Step 5: Add Groq API Key

Open app.py and replace the API key placeholder:

GROQ_API_KEY = "YOUR_GROQ_API_KEY"

Step 6: Run the Application
streamlit run app.py


The app will open in your browser automatically.

How to Use the Application

Upload your resume (PDF / JPG / PNG)

Select the target job role

Click Analyze Resume

View:

ATS score

Section-wise analysis

AI-generated resume feedback

Limitations

ATS score is an approximation, not an official ATS result

Accuracy depends on resume clarity and formatting

Image resumes work best when text is clear

Future Enhancements

Resume vs Job Description matching

Download ATS report as PDF

Keyword optimization suggestions

Improved resume scoring logic

Conclusion

This project shows how AI can be used to analyze resumes and give meaningful feedback.
It is simple, practical, and useful for students preparing for jobs or internships.
