from fastapi import FastAPI
from .routers.resume import router as resume_router

app = FastAPI(title="Resume Matcher API", version="2.0.0")

# Single unified route
app.include_router(resume_router, prefix="/resume", tags=["Resume & Recommendations"])

@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}
