from PyPDF2 import PdfReader
from typing import BinaryIO

def extract_text_from_pdf(file_obj: BinaryIO) -> str:
    reader = PdfReader(file_obj)
    parts = []
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            parts.append(extracted)
    return ("\n".join(parts)).strip().lower()
