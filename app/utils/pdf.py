from PyPDF2 import PdfReader
from typing import BinaryIO

def extract_text_from_pdf(file_obj: BinaryIO) -> str:
    """Extract text simply and lower-case it. Keep it short and clear."""
    reader = PdfReader(file_obj)
    parts = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            parts.append(text)
    return '\n'.join(parts).strip().lower()
