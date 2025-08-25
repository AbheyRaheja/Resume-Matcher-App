import os
import pickle
import numpy as np
import pandas as pd
from typing import List, Tuple

from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier, LogisticRegression
from sklearn.naive_bayes import ComplementNB
from sklearn.ensemble import VotingClassifier
from sklearn.preprocessing import LabelEncoder

from app.config import settings
from app.utils.text import clean_resume

# Singleton-like module state
_pipeline = None
_label_encoder = None
_labels = None

def _build_pipeline():
    # Ensemble models (your tuned versions)
    clf_sgd = SGDClassifier(
        loss="log_loss",
        max_iter=3000,
        alpha=1e-4,
        class_weight="balanced",
        random_state=42
    )
    clf_nb = ComplementNB(alpha=0.5)
    clf_lr = LogisticRegression(
        max_iter=3000,
        solver="saga",
        C=2.0,
        class_weight="balanced",
        random_state=42
    )
    voting = VotingClassifier(
        estimators=[('sgd', clf_sgd), ('nb', clf_nb), ('lr', clf_lr)],
        voting='soft',
        n_jobs=-1
    )
    pipe = make_pipeline(
        TfidfVectorizer(
            lowercase=True,
            analyzer="word",
            ngram_range=(1,2),
            min_df=2,
            max_df=0.9
        ),
        voting
    )
    return pipe

def _train_and_save():
    global _pipeline, _label_encoder, _labels

    df = pd.read_csv(settings.DATASET_PATH)
    df = df.drop_duplicates(subset=["Resume"]).reset_index(drop=True)
    df["cleaned_resume"] = df["Resume"].apply(clean_resume)

    le = LabelEncoder()
    y = le.fit_transform(df["Category"])
    X = df["cleaned_resume"]

    pipe = _build_pipeline()
    pipe.fit(X, y)

    os.makedirs(os.path.dirname(settings.PIPELINE_PATH), exist_ok=True)
    with open(settings.PIPELINE_PATH, "wb") as f:
        pickle.dump({"pipe": pipe, "label_encoder": le}, f)

    _pipeline = pipe
    _label_encoder = le
    _labels = le.classes_.tolist()

def _load_or_train():
    global _pipeline, _label_encoder, _labels
    if _pipeline is not None:
        return

    if os.path.exists(settings.PIPELINE_PATH):
        with open(settings.PIPELINE_PATH, "rb") as f:
            bundle = pickle.load(f)
        _pipeline = bundle["pipe"]
        _label_encoder = bundle["label_encoder"]
        _labels = _label_encoder.classes_.tolist()
    else:
        _train_and_save()

def predict_topk(text: str, k: int) -> List[Tuple[str, float]]:
    """
    Returns [(label_name, probability), ...] of length k.
    """
    _load_or_train()
    cleaned = clean_resume(text)
    proba = _pipeline.predict_proba([cleaned])[0]  # shape: (n_classes,)
    k = min(k, proba.shape[0])
    idx = np.argsort(proba)[::-1][:k]
    return [(str(_labels[i]), float(proba[i])) for i in idx]
