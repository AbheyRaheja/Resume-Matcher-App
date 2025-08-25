import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # paths
    DATASET_PATH: str = os.path.abspath("data/UpdatedResumeDataSet.csv")
    PIPELINE_PATH: str = os.path.abspath("models/pipeline.pkl")  # <-- add this

    # Adzuna
    ADZUNA_APP_ID: str = ""
    ADZUNA_APP_KEY: str = ""

    # SentenceTransformer model
    EMBED_MODEL_NAME: str = "all-MiniLM-L6-v2"

    # Recs defaults
    DEFAULT_LOCATION: str = "india"
    DEFAULT_JOBS_PER_FIELD: int = 10
    DEFAULT_TOTAL_JOBS: int = 10
    TOP_K_PREDICTIONS: int = 2

    class Config:
        env_file = ".env"

settings = Settings()
