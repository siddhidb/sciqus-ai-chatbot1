from sentence_transformers import SentenceTransformer
import faiss, os, pickle

model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.IndexFlatL2(384)
store = []

def add(text):
    emb = model.encode([text])
    index.add(emb)
    store.append(text)

pickle.dump((index, store), open("data/embeddings/store.pkl","wb"))
