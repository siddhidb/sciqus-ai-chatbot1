from pathlib import Path
import pdfplumber


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text from a PDF safely.
    """
    text_parts = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)

    return "\n".join(text_parts)
