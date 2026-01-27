from pathlib import Path

RAW_DIR = Path("data/raw")
CHUNK_DIR = Path("data/chunks")

CHUNK_DIR.mkdir(parents=True, exist_ok=True)

def chunk_text(text, chunk_size=400, overlap=50):
    words = text.split()
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = words[start:end]
        yield " ".join(chunk)
        start += chunk_size - overlap

for file in RAW_DIR.glob("*.txt"):
    text = file.read_text(encoding="utf-8").strip()

    if not text:
        continue

    chunks = list(chunk_text(text))

    for i, chunk in enumerate(chunks):
        out_file = CHUNK_DIR / f"{file.stem}_chunk_{i}.txt"
        out_file.write_text(chunk, encoding="utf-8")

    print(f"✅ Chunked: {file.name} ({len(chunks)} chunks)")
