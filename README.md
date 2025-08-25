# 📄 Resume Job Matcher

Resume Job Matcher is a web application that takes your resume (PDF) as input and recommends the most relevant jobs based on your skills and experience. The backend handles text extraction and job matching, while the frontend provides a simple and user-friendly interface to view recommendations.

---

## Features

- Upload your resume in PDF format.
- Automatic text extraction from the resume.
- Job recommendations based on extracted skills and experience.
- Clean and interactive Streamlit frontend.
- Clickable links to apply directly for recommended jobs.

---

## Tech Stack

- **Frontend:** Streamlit  
- **Backend:** FastAPI  
- **Python Libraries:** `requests`, `pydantic`, `uvicorn`, `pdfminer` (or any PDF parser)  
- **Deployment:** Localhost / Cloud (optional)

---


## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/resume-matcher-app.git
cd resume-matcher-app

python -m venv .venv
source .venv/bin/activate    # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

uvicorn app.main:app --reload

streamlit run frontend/frontend.py

Usage

Open the Streamlit app in your browser.
Upload your resume in PDF format.
Wait for the backend to process the file.
View the recommended jobs with location and preview.
Click Apply Here to open the job application link.