from typing import List, Optional
from pydantic import BaseModel

class UploadResumeResponse(BaseModel):
    text: str

class PredictRequest(BaseModel):
    text: str

class Prediction(BaseModel):
    label: str
    probability: float

class PredictResponse(BaseModel):
    predictions: List[Prediction]

class RecommendRequest(BaseModel):
    text: str
    location: Optional[str] = None
    jobs_per_field: Optional[int] = None
    total_jobs: Optional[int] = None
    top_k: Optional[int] = None

class JobItem(BaseModel):
    field: str
    title: str
    location: str
    preview: str
    similarity: float
    probability: float
    weighted_score: float
    link: str

class RecommendResponse(BaseModel):
    predictions: List[Prediction]
    results: List[JobItem]
