import os, pickle, numpy as np
from typing import List, Tuple
from app.config import settings
from app.utils.text import clean_resume

_pipeline = None
_labels = None

def _load():
    global _pipeline, _labels
    if _pipeline is not None:
        return
    if os.path.exists(settings.PIPELINE_PATH):
        with open(settings.PIPELINE_PATH,'rb') as f:
            bundle = pickle.load(f)
        _pipeline = bundle.get('pipe')
        _labels = bundle.get('label_encoder').classes_.tolist()
    else:
        raise RuntimeError('Model not trained. Run the training script first.')

def predict_topk(text: str, k:int=2) -> List[Tuple[str,float]]:
    _load()
    cleaned = clean_resume(text)
    proba = _pipeline.predict_proba([cleaned])[0]
    idx = np.argsort(proba)[::-1][:k]
    return [(str(_labels[i]), float(proba[i])) for i in idx]
