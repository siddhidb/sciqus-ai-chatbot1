# app/ingestion/embed_store.py

import uuid
from datetime import datetime
from app.core.vectorstore import get_collection


def embed_and_store(chunks, metadata: dict):
    print("🔥 embed_and_store CALLED")
    print("🔥 Number of chunks received:", len(chunks))

    if not chunks:
        print("❌ NO CHUNKS — EXITING")
        return

    collection = get_collection()
    print("🔥 Using collection:", collection.name)

    ids = [str(uuid.uuid4()) for _ in chunks]

    collection.add(
        documents=chunks,
        metadatas=[{
            **metadata,
            "ingested_at": datetime.utcnow().isoformat()
        } for _ in chunks],
        ids=ids
    )

    print("✅ collection.add() EXECUTED & PERSISTED")
