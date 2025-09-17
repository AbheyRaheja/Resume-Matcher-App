from fastapi import FastAPI, UploadFile, File, HTTPException
from app.utils.pdf import extract_text_from_pdf
from app.utils.text import clean_resume
from app.utils.jobs import fetch_jobs
from app.services.ml_simple import predict_topk
from app.config import settings

app = FastAPI(title="Resume Matcher - Explainable")


@app.post("/resume/upload")
async def upload(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF allowed")

    # 1. Extract + clean text
    text = extract_text_from_pdf(file.file)
    clean_text = clean_resume(text)

    # 2. Predict top categories
    preds = predict_topk(clean_text, k=settings.TOP_K_PREDICTIONS)
    predictions = [{"label": l, "probability": float(p)} for l, p in preds]

    # 3. Fetch jobs for top prediction
    top_label = predictions[0]["label"]
    jobs = fetch_jobs(top_label, location="india", results_per_page=5)

    return {"predictions": predictions, "jobs": jobs}


@app.get("/health")
def health():
    return {"status": "ok"}
