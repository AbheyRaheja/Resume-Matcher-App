import os
import requests
import numpy as np
from typing import List, Dict, Tuple
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

from app.config import settings

# lazy-load embedder
_embedder = None
def _get_embedder():
    global _embedder
    if _embedder is None:
        _embedder = SentenceTransformer(settings.EMBED_MODEL_NAME)
    return _embedder

def _embed(text: str):
    model = _get_embedder()
    return model.encode([text], convert_to_tensor=True).cpu().numpy()

def fetch_jobs(query: str, location: str, num_jobs: int) -> List[Dict]:
    app_id = settings.ADZUNA_APP_ID
    app_key = settings.ADZUNA_APP_KEY
    if not app_id or not app_key:
        raise RuntimeError("Adzuna credentials missing. Set ADZUNA_APP_ID and ADZUNA_APP_KEY in .env")

    url = "https://api.adzuna.com/v1/api/jobs/in/search/1"
    params = {
        "app_id": app_id,
        "app_key": app_key,
        "results_per_page": num_jobs,
        "what": query,
        "where": location,
        "content-type": "application/json"
    }
    r = requests.get(url, params=params, timeout=20)
    r.raise_for_status()
    data = r.json()
    jobs = []
    for job in data.get("results", []):
        jobs.append({
            "title": job.get("title", "N/A"),
            "location": job.get("location", {}).get("display_name", "N/A"),
            "description": job.get("description", "") or "",
            "link": job.get("redirect_url", "N/A")
        })
    return jobs

def weighted_job_selection(resume_text: str,
                           predictions: List[Tuple[str, float]],
                           location: str,
                           jobs_per_field: int,
                           total_jobs: int) -> List[Dict]:
    """
    Fetch jobs for all predicted categories and merge them into one ranked list.
    Score = cosine_similarity(resume, job_desc) * model_probability
    """
    resume_vec = _embed(resume_text)
    all_jobs: List[Dict] = []

    for field, prob in predictions:
        jobs = fetch_jobs(query=field, location=location, num_jobs=jobs_per_field)
        for job in jobs:
            job_vec = _embed(job["description"])
            sim = float(cosine_similarity(resume_vec, job_vec)[0][0])
            weighted = sim * float(prob)
            all_jobs.append({
                "field": field,
                "title": job["title"],
                "location": job["location"],
                "preview": job["description"][:300].replace("\n", " "),
                "similarity": sim,
                "probability": float(prob),
                "weighted_score": weighted,
                "link": job["link"]
            })

    all_jobs.sort(key=lambda x: x["weighted_score"], reverse=True)
    return all_jobs[:total_jobs]
