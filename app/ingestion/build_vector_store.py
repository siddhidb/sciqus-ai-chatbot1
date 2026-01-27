from pathlib import Path
import pickle
import faiss
from sentence_transformers import SentenceTransformer

CHUNK_DIR = Path("data/chunks")
VECTOR_DIR = Path("data/vector")

VECTOR_DIR.mkdir(parents=True, exist_ok=True)

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

texts = []
metadata = []

for file in CHUNK_DIR.glob("*.txt"):
    text = file.read_text(encoding="utf-8").strip()
    if not text:
        continue

    texts.append(text)
    metadata.append({
        "source_file": file.name
    })

print(f"Embedding {len(texts)} chunks...")

embeddings = model.encode(texts, show_progress_bar=True)

# Create FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# Save index + metadata
faiss.write_index(index, str(VECTOR_DIR / "index.faiss"))

with open(VECTOR_DIR / "metadata.pkl", "wb") as f:
    pickle.dump(metadata, f)

with open(VECTOR_DIR / "texts.pkl", "wb") as f:
    pickle.dump(texts, f)

print("✅ Vector store created successfully")
