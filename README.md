# 📄 Resume Matcher App

An **AI-powered Resume-to-Job Matcher** that:
- Extracts text from uploaded resumes.
- Predicts the top 3 job categories using a trained ML pipeline.
- Fetches live job postings via the **Adzuna API**.
- Ranks jobs by similarity between resume content and job descriptions.
- Provides a simple **Streamlit frontend** and a **FastAPI backend**.

---

## 🚀 Features
- **FastAPI backend** for prediction and job recommendation.
- **Streamlit frontend** for an interactive UI.
- **ML pipeline** with TF-IDF + Logistic Regression/SGD/Naive Bayes (ensemble).
- Support for **experimenting** with XGBoost, CatBoost, LightGBM.
- **MLOps integrations**:
  - Docker containerization.
  - MLflow for experiment tracking.
  - DVC for dataset versioning.
  - GitHub Actions for CI/CD.
  - AWS-ready

---

## 📂 Project Structure

Resume-Matcher-App/
├── app/
│ ├── routers/ # API routes
│ ├── services/ # ML & job recommendation logic
│ ├── utils/ # PDF/text processing
│ ├── models/ # Pydantic schemas
│ ├── config.py # Configuration (.env support)
│ └── main.py # FastAPI entrypoint
├── frontend/
│ └── frontend.py # Streamlit app
├── data/ # Resume dataset
├── models/ # Saved ML pipeline
├── requirements.txt # Python dependencies
├── Dockerfile # Docker container
├── dvc.yaml # DVC pipeline config
├── .github/workflows/ # CI/CD pipelines
├── README.md # Project documentation
└── .env.example # Example environment variables


---

## ⚙️ Setup Instructions

### 1️⃣ Clone repo & install dependencies
```bash
git clone https://github.com/AbheyRaheja/Resume-Matcher-App.git
pip install -r requirements.txt

2️⃣ Environment variables

Create a .env file in the project root:

ADZUNA_APP_ID=your_app_id
ADZUNA_APP_KEY=your_app_key
DEFAULT_LOCATION=india

3️⃣ Run backend (FastAPI)

uvicorn app.main:app --reload

API will be available at:
👉 http://127.0.0.1:8000/docs

4️⃣ Run frontend (Streamlit)

streamlit run frontend/frontend.py

Frontend UI will be available at:
👉 http://localhost:8501

Machine Learning

ML pipeline: TF-IDF + Ensemble (SGD + Naive Bayes + Logistic Regression).
Experimentation: Try XGBoost, LightGBM, CatBoost (app/services/ml_experiments.py).
Labels are trained from data/UpdatedResumeDataSet.csv.

MLOps & Deployment

Docker
Build and run the container:

docker build -t resume-matcher .
docker run -p 8000:8000 resume-matcher


MLflow Tracking
Launch MLflow locally:

mlflow ui --host 0.0.0.0 --port 5000


DVC for Data Versioning

dvc init
dvc add data/UpdatedResumeDataSet.csv
git add data/UpdatedResumeDataSet.csv.dvc .gitignore
git commit -m "Track dataset with DVC"

CI/CD
GitHub Actions workflow (.github/workflows/ci-cd.yml) runs tests, builds Docker images, and can deploy to AWS.
