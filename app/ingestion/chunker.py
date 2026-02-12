# app/ingestion/chunker.py

def chunk_text(text: str, size: int = 400, overlap: int = 50):
    """
    Split text into overlapping word chunks.
    """

    if not text:
        return []

    words = text.split()
    chunks = []

    start = 0
    while start < len(words):
        end = start + size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += size - overlap

    return chunks
