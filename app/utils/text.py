import re
import nltk
from nltk.corpus import stopwords

# Ensure stopwords available at import time
try:
    _ = stopwords.words("english")
except LookupError:
    nltk.download("stopwords", quiet=True)

STOPWORDS = set(stopwords.words("english"))

def clean_resume(text: str) -> str:
    text = re.sub(r"http\S+\s*", " ", text)
    text = re.sub(r"RT|cc", " ", text)
    text = re.sub(r"#\S+", " ", text)
    text = re.sub(r"@\S+", " ", text)
    text = re.sub(r"[%s]" % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), " ", text)
    text = re.sub(r"[^\x00-\x7f]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def extract_skills(text: str):
    words = re.findall(r"\b[a-zA-Z][a-zA-Z]+\b", text.lower())
    filtered = [w for w in words if w not in STOPWORDS and len(w) > 2]
    return list(set(filtered))
