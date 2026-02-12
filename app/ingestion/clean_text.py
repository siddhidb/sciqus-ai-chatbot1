# app/ingestion/clean_text.py

from bs4 import BeautifulSoup


def clean_text(text: str) -> str:
    """
    Clean raw HTML or plain text.

    - Removes navigation, footer, scripts, styles
    - Normalizes whitespace
    - Returns clean text suitable for chunking & embeddings
    """

    if not text:
        return ""

    soup = BeautifulSoup(text, "html.parser")

    # Remove unwanted tags
    for tag in soup(["nav", "footer", "script", "style"]):
        tag.decompose()

    # Extract visible text
    cleaned_text = soup.get_text(separator=" ")

    # Normalize whitespace
    cleaned_text = " ".join(cleaned_text.split())

    return cleaned_text


# from bs4 import BeautifulSoup
# from pathlib import Path

# RAW = Path("data/raw")
# OUT = Path("data/cleaned")
# OUT.mkdir(exist_ok=True)

# for file in RAW.glob("*.html"):
#     soup = BeautifulSoup(file.read_text(), "html.parser")
#     for tag in soup(["nav","footer","script","style"]):
#         tag.decompose()
#     text = soup.get_text(separator="\n")
#     (OUT / file.name.replace(".html",".txt")).write_text(text)
