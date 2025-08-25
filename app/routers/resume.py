from fastapi import APIRouter, UploadFile, File, HTTPException
from app.utils.pdf import extract_text_from_pdf
from app.models.schemas import RecommendResponse, Prediction, JobItem
from app.services.ml import predict_topk
from app.services.jobs import weighted_job_selection
from app.config import settings

router = APIRouter()

@router.post("/upload", response_model=RecommendResponse)
async def upload_resume(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    try:
        # 1. Extract text from resume
        text = extract_text_from_pdf(file.file)
        if not text:
            raise HTTPException(status_code=400, detail="Could not extract text from PDF.")

        # 2. Predict top-k categories
        preds = predict_topk(text, k=settings.TOP_K_PREDICTIONS)

        # 3. Fetch + rank jobs
        results = weighted_job_selection(
            resume_text=text,
            predictions=preds,
            location=settings.DEFAULT_LOCATION,
            jobs_per_field=settings.DEFAULT_JOBS_PER_FIELD,
            total_jobs=settings.DEFAULT_TOTAL_JOBS
        )

        # 4. Return predictions + job list
        return RecommendResponse(
            predictions=[Prediction(label=l, probability=p) for l, p in preds],
            results=[JobItem(**r) for r in results]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
