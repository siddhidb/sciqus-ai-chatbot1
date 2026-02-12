from fastapi import APIRouter, Header, HTTPException, UploadFile, File
import os
import shutil

from app.ingestion.ingest import ingest_document, ingest_website
from app.core.vectorstore import delete_by_source
from app.utils.source_registry import (
    register_source,
    list_sources,
    remove_source
)

router = APIRouter(prefix="/admin", tags=["Admin"])

# =========================
# CONFIG
# =========================
ADMIN_API_KEY = os.getenv("ADMIN_API_KEY")

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# =========================
# ADMIN AUTH
# =========================
def verify_admin(x_api_key: str):
    if not ADMIN_API_KEY:
        raise HTTPException(status_code=500, detail="ADMIN_API_KEY not set")

    if x_api_key != ADMIN_API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized admin")




@router.post("/ingest/document")
def ingest_document_api(
    file: UploadFile = File(...),
    x_api_key: str = Header(...)
):
    verify_admin(x_api_key)

    allowed = (".pdf", ".docx", ".txt")
    if not file.filename.lower().endswith(allowed):
        raise HTTPException(
            status_code=400,
            detail="Only PDF, DOCX, or TXT files allowed"
        )

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    ingest_document(
        file_path=file_path,
        source_name=file.filename,
        uploaded_by="admin"
    )

    register_source(
        source_name=file.filename,
        source_type="document",
        location=file_path
    )

    return {
        "status": "success",
        "source_name": file.filename
    }


# # =========================
# # 📄 PDF INGESTION
# # =========================
# @router.post("/ingest/pdf")
# def ingest_pdf_api(
#     file: UploadFile = File(...),
#     x_api_key: str = Header(...)
# ):
#     verify_admin(x_api_key)

#     if not file.filename.lower().endswith(".pdf"):
#         raise HTTPException(status_code=400, detail="Only PDF files allowed")

#     file_path = os.path.join(UPLOAD_DIR, file.filename)

#     with open(file_path, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)

#     ingest_pdf(
#         pdf_path=file_path,
#         source_name=file.filename,
#         uploaded_by="admin"
#     )

#     register_source(
#         source_name=file.filename,
#         source_type="pdf",
#         location=file_path
#     )

#     return {
#         "status": "success",
#         "source_name": file.filename
#     }


# =========================
# 🌐 WEBSITE INGESTION
# =========================
@router.post("/ingest/website")
def ingest_website_api(
    base_url: str,
    x_api_key: str = Header(...)
):
    verify_admin(x_api_key)

    source_name = base_url  # URL itself is the source key

    ingest_website(
        base_url=base_url,
        source_name=source_name
    )

    register_source(
        source_name=source_name,
        source_type="website",
        location=base_url
    )

    return {
        "status": "success",
        "source_name": source_name
    }


# =========================
# 🗑️ DELETE SOURCE (PDF / WEBSITE / DOC)
# =========================
@router.delete("/delete/source")
def delete_source_api(
    source_name: str,
    x_api_key: str = Header(...)
):
    verify_admin(x_api_key)

    sources = list_sources()
    source = next((s for s in sources if s["source_name"] == source_name), None)

    if not source:
        raise HTTPException(status_code=404, detail="Source not found")

    # 1️⃣ Delete vectors from Chroma
    delete_by_source(source_name)

    # 2️⃣ Delete uploaded file if local (PDF / DOC)
    if source["type"] in ("pdf", "doc"):
        if os.path.exists(source["location"]):
            os.remove(source["location"])
            print(f"🗑️ Deleted file: {source['location']}")

    # 3️⃣ Remove from registry
    remove_source(source_name)

    return {
        "status": "deleted",
        "source_name": source_name
    }


# =========================
# 📋 LIST ALL SOURCES
# =========================
@router.get("/sources")
def list_all_sources(x_api_key: str = Header(...)):
    verify_admin(x_api_key)
    return list_sources()


