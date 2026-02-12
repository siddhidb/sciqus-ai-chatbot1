# app/debug_chroma.py

from app.core.vectorstore import get_collection

collection = get_collection()

print("📦 Collection:", collection.name)
print("📊 Total documents:", collection.count())

