# # app/ingestion/ingest.py
# from app.ingestion.extract_pdf import extract_text_from_pdf
# from app.ingestion.clean_text import clean_text
# from app.ingestion.chunker import chunk_text
# from app.ingestion.embed_store import embed_and_store
# from app.ingestion.crawl_site import crawl_website
# from datetime import datetime
# import os
# from app.ingestion.document_loader import load_document
# from app.core.vectorstore import get_collection

# def ingest_website(
#     base_url: str,
#     source_name: str,
#     uploaded_by: str = "admin"
# ):
#     """
#     DEFAULT knowledge ingestion.
#     Website is the primary knowledge source.
#     """

#     print("🌐 Crawling website...")
#     pages = crawl_website(base_url)

#     all_chunks = []

#     for page in pages:
#         cleaned = clean_text(page["text"])
#         chunks = chunk_text(cleaned)
#         all_chunks.extend(chunks)

#     print(f"🧩 Total chunks created: {len(all_chunks)}")

#     if not all_chunks:
#         print("❌ No chunks created. Ingestion stopped.")
#         return

#     embed_and_store(
#         chunks=all_chunks,
#         metadata={
#             "source": "website",
#             "source_name": source_name,
#             "uploaded_by": uploaded_by,
#         }
#     )

#     print("✅ Website knowledge embedded successfully")


# def ingest_pdf(
#     pdf_path: str,
#     source_name: str,
#     uploaded_by: str = "admin"
# ):
#     """
#     Admin-only PDF ingestion.
#     """

#     raw_text = extract_text_from_pdf(pdf_path)
#     cleaned_text = clean_text(raw_text)
#     chunks = list(chunk_text(cleaned_text))

#     if not chunks:
#         return

#     embed_and_store(
#         chunks=chunks,
#         metadata={
#             "source": "pdf",
#             "source_name": source_name,
#             "uploaded_by": uploaded_by,
#             "ingested_at": datetime.utcnow().isoformat(),
#         }
#     )

#     print("✅ PDF/docs knowledge embedded successfully")


# def ingest_document(
#     file_path: str,
#     source_name: str,
#     uploaded_by: str
# ):
#     text = load_document(file_path)

#     if not text.strip():
#         raise ValueError("Document contains no readable text")

#     # simple chunking (you can improve later)
#     chunks = [
#         text[i:i+800]
#         for i in range(0, len(text), 800)
#         if len(text[i:i+800].strip()) > 100
#     ]

#     collection = get_collection()

#     collection.add(
#         documents=chunks,
#         metadatas=[{"source": source_name}] * len(chunks),
#         ids=[f"{source_name}_{i}" for i in range(len(chunks))]
#     )

#     print(f"✅ Document ingested: {source_name}")

# app/ingestion/ingest.py
# app/ingestion/ingest.py
import os
import requests
from typing import List
from app.core.vectorstore import get_collection
from app.ingestion.document_loader import load_document

# =========================
# TEXT CHUNKER
# =========================
def chunk_text(text: str, chunk_size: int = 800, overlap: int = 100) -> List[str]:
    chunks = []
    start = 0
    text = text.strip()

    print("🧾 Raw text length:", len(text))

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if len(chunk) > 80:
            chunks.append(chunk)

        start = end - overlap

    print("🧩 Chunks created:", len(chunks))
    return chunks

# =========================
# DOCUMENT INGESTION
# =========================
def ingest_document(file_path: str, source_name: str, uploaded_by: str):
    print("📄 Ingesting document:", file_path)

    if not os.path.exists(file_path):
        raise FileNotFoundError(file_path)

    text = load_document(file_path)

    if not text or len(text.strip()) < 50:
        raise ValueError("❌ Empty or unreadable document")

    chunks = chunk_text(text)
    if not chunks:
        raise ValueError("❌ No valid chunks")

    collection = get_collection()

    collection.add(
        documents=chunks,
        metadatas=[{"source": source_name}] * len(chunks),
        ids=[f"{source_name}_{i}" for i in range(len(chunks))]
    )

    print(f"✅ Document ingested: {source_name}")
    print("📦 Total vectors:", collection.count())

# =========================
# WEBSITE INGESTION
# =========================
def ingest_website(base_url: str, source_name: str):
    print("🌐 Ingesting website:", base_url)

    response = requests.get(base_url, timeout=10)
    response.raise_for_status()

    chunks = chunk_text(response.text)
    if not chunks:
        raise ValueError("❌ Website content empty")

    collection = get_collection()

    collection.add(
        documents=chunks,
        metadatas=[{"source": source_name}] * len(chunks),
        ids=[f"{source_name}_{i}" for i in range(len(chunks))]
    )

    print(f"✅ Website ingested: {source_name}")
