import re, nltk
from nltk.corpus import stopwords
try:
    _ = stopwords.words('english')
except LookupError:
    nltk.download('stopwords', quiet=True)
STOPWORDS = set(stopwords.words('english'))

def clean_resume(text: str) -> str:
    text = re.sub(r'http\S+', ' ', text)
    text = re.sub(r'[^\x00-\x7f]', ' ', text)
    text = re.sub(r'[%s]' % re.escape("!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"), ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip().lower()
