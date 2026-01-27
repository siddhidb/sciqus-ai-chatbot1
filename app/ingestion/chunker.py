def chunk_text(text, size=400):
    words = text.split()
    for i in range(0, len(words), size):
        yield " ".join(words[i:i+size])
