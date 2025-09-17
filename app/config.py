import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Project settings
    DATASET_PATH: str = os.path.abspath("data/UpdatedResumeDataSet.csv")
    PIPELINE_PATH: str = os.path.abspath("models/pipeline.pkl")
    EMBED_MODEL_NAME: str = "all-MiniLM-L6-v2"
    TOP_K_PREDICTIONS: int = 3

    # Adzuna API credentials
    ADZUNA_APP_ID: str = ""
    ADZUNA_APP_KEY: str = ""

    class Config:
        env_file = ".env"   # tells pydantic to load from .env

settings = Settings()

if __name__ == "__main__":
    print("Dataset Path:", settings.DATASET_PATH)
    print("Pipeline Path:", settings.PIPELINE_PATH)
    print("Embed Model:", settings.EMBED_MODEL_NAME)
    print("Top K:", settings.TOP_K_PREDICTIONS)
    print("Adzuna App ID:", settings.ADZUNA_APP_ID)
    print("Adzuna App Key:", settings.ADZUNA_APP_KEY)
