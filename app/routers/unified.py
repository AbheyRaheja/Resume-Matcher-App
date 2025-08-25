from fastapi import APIRouter, UploadFile, File, HTTPException
from app.schemas import RecommendResponse, PredictionItem, RecommendedJob
from app.config import settings
from app.utils.pdf import extract_text_from_pdf_bytes
from app.services.ml import predict_topk
from app.services.jobs import weighted_job_selection

router = APIRouter(prefix="/api", tags=["Unified"])

@router.get("/health")
def health():
    return {"status": "ok"}

@router.post("/recommendations/upload", response_model=RecommendResponse)
async def upload_resume_and_recommend(file: UploadFile = File(...)):
    """
    Upload a resume (PDF/TXT), get top-2 predicted fields, fetch jobs for both,
    compute similarity & weighted ranking, and return one unified list.
    """
    # 1) Extract resume text
    data = await file.read()
    content_type = (file.content_type or "").lower()

    if content_type in ["application/pdf", "application/x-pdf", "pdf"]:
        try:
            resume_text = extract_text_from_pdf_bytes(data)
        except Exception:
            raise HTTPException(status_code=400, detail="Failed to parse PDF")
    else:
        # Assume plain text if not PDF
        try:
            resume_text = data.decode("utf-8", errors="ignore")
        except Exception:
            raise HTTPException(status_code=400, detail="Failed to parse text file")

    if not resume_text.strip():
        raise HTTPException(status_code=400, detail="Empty resume content")

    # 2) Predict top-K fields using trained model
    preds = predict_topk(resume_text, settings.TOP_K_PREDICTIONS)  # List[(field, prob)]

    # 3) Fetch & rank jobs with weighted similarity
    jobs = weighted_job_selection(
        resume_text=resume_text,
        predictions=preds,
        location=settings.DEFAULT_LOCATION,
        jobs_per_field=settings.JOBS_PER_FIELD,
        total_jobs=settings.TOTAL_RETURN_JOBS,
    )

    # 4) Build response
    return RecommendResponse(
        predictions=[PredictionItem(field=f, probability=p) for f, p in preds],
        jobs=[RecommendedJob(**j) for j in jobs]
    )
