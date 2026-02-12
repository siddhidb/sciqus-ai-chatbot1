# # # # import os
# # # # import chromadb
# # # # from pathlib import Path
# # # # from sentence_transformers import SentenceTransformer

# # # # # =========================
# # # # # CONFIG
# # # # # =========================
# # # # CHROMA_DIR = os.getenv("CHROMA_DB_PATH", "/app/data/chroma")
# # # # COLLECTION_NAME = "sciqus_knowledge"

# # # # os.makedirs(CHROMA_DIR, exist_ok=True)

# # # # # # =========================
# # # # # # EMBEDDING MODEL (OFFLINE, LOCAL)
# # # # # # =========================
# # # # # MODEL_PATH = Path(
# # # # #     "/app/.cache/huggingface/hub/models--sentence-transformers--all-MiniLM-L6-v2"
# # # # # )

# # # # # if not MODEL_PATH.exists():
# # # # #     raise RuntimeError(
# # # # #         f"❌ Sentence-Transformers model not found at {MODEL_PATH}"
# # # # #     )

# # # # # _embedding_model = SentenceTransformer(
# # # # #     str(MODEL_PATH),
# # # # #     device="cpu"
# # # # # )

# # # # # def embedding_fn(texts: list[str]) -> list[list[float]]:
# # # # #     """
# # # # #     Chroma-compatible embedding function.
# # # # #     """
# # # # #     return _embedding_model.encode(
# # # # #         texts,
# # # # #         show_progress_bar=False,
# # # # #         convert_to_numpy=True
# # # # #     ).tolist()


# # # # # =========================
# # # # # EMBEDDING MODEL (DOCKER + LOCAL SAFE)
# # # # # =========================
# # # # MODEL_NAME = "all-MiniLM-L6-v2"

# # # # HF_HOME = os.getenv("HF_HOME")  # set in Docker, not locally
# # # # DOCKER_MODEL_PATH = (
# # # #     Path(HF_HOME) / "huggingface" / "hub" /
# # # #     "models--sentence-transformers--all-MiniLM-L6-v2"
# # # #     if HF_HOME else None
# # # # )

# # # # def load_embedding_model():
# # # #     # 1️⃣ Docker path (offline, guaranteed)
# # # #     if DOCKER_MODEL_PATH and DOCKER_MODEL_PATH.exists():
# # # #         return SentenceTransformer(
# # # #             str(DOCKER_MODEL_PATH),
# # # #             device="cpu"
# # # #         )

# # # #     # 2️⃣ Local dev fallback (auto-download allowed)
# # # #     if os.getenv("ENV") != "production":
# # # #         return SentenceTransformer(
# # # #             MODEL_NAME,
# # # #             device="cpu"
# # # #         )

# # # #     # 3️⃣ Production safety net
# # # #     raise RuntimeError(
# # # #         "❌ Embedding model not available and auto-download disabled"
# # # #     )

# # # # _embedding_model = load_embedding_model()

# # # # def embedding_fn(texts: list[str]) -> list[list[float]]:
# # # #     """
# # # #     Chroma-compatible embedding function.
# # # #     """
# # # #     return _embedding_model.encode(
# # # #         texts,
# # # #         show_progress_bar=False,
# # # #         convert_to_numpy=True
# # # #     ).tolist()

# # # # # =========================
# # # # # SINGLE PERSISTENT CLIENT
# # # # # =========================
# # # # _client = chromadb.PersistentClient(path=CHROMA_DIR)

# # # # def get_collection(name: str = COLLECTION_NAME):
# # # #     """
# # # #     Returns (or creates) the Chroma collection.
# # # #     """
# # # #     return _client.get_or_create_collection(
# # # #         name=name,
# # # #         embedding_function=embedding_fn
# # # #     )

# # # # def delete_by_source(source_name: str):
# # # #     """
# # # #     Delete all vectors belonging to a source.
# # # #     """
# # # #     collection = get_collection()
# # # #     collection.delete(where={"source": source_name})
# # # #     print(f"🗑️ Deleted knowledge for source: {source_name}")
# # # import os
# # # import chromadb
# # # from pathlib import Path
# # # from sentence_transformers import SentenceTransformer

# # # # =========================
# # # # CONFIG
# # # # =========================
# # # CHROMA_DIR = os.getenv("CHROMA_DB_PATH", "vectorstore")
# # # COLLECTION_NAME = "sciqus_knowledge_v2"

# # # os.makedirs(CHROMA_DIR, exist_ok=True)

# # # # =========================
# # # # EMBEDDING MODEL (DOCKER + LOCAL SAFE)
# # # # =========================
# # # MODEL_NAME = "all-MiniLM-L6-v2"

# # # HF_HOME = os.getenv("HF_HOME")  # set in Docker
# # # DOCKER_MODEL_PATH = (
# # #     Path(HF_HOME)
# # #     / "huggingface"
# # #     / "hub"
# # #     / "models--sentence-transformers--all-MiniLM-L6-v2"
# # #     if HF_HOME
# # #     else None
# # # )

# # # def load_embedding_model():
# # #     """
# # #     Load Sentence-Transformers model safely for Docker and local dev.
# # #     """
# # #     # Docker: offline, preloaded
# # #     if DOCKER_MODEL_PATH and DOCKER_MODEL_PATH.exists():
# # #         return SentenceTransformer(str(DOCKER_MODEL_PATH), device="cpu")

# # #     # Local dev: allow download
# # #     if os.getenv("ENV") != "production":
# # #         return SentenceTransformer(MODEL_NAME, device="cpu")

# # #     # Production safety
# # #     raise RuntimeError(
# # #         "❌ Embedding model not available and auto-download disabled"
# # #     )

# # # _embedding_model = load_embedding_model()

# # # # =========================
# # # # CHROMA EMBEDDING FUNCTION (FULL INTERFACE)
# # # # =========================
# # # class SentenceTransformerEmbeddingFunction:
# # #     """
# # #     Fully compliant ChromaDB embedding function
# # #     using Sentence-Transformers.
# # #     """

# # #     def __init__(self, model: SentenceTransformer):
# # #         self.model = model

# # #     def __call__(self, input):
# # #         return self.embed_documents(input)

# # #     def embed_documents(self, input):
# # #         if not input:
# # #             return []

# # #         return self.model.encode(
# # #             list(input),
# # #             show_progress_bar=False,
# # #             convert_to_numpy=True
# # #         ).tolist()

# # #     def embed_query(self, input):
# # #         # Chroma may pass string OR list
# # #         if isinstance(input, list):
# # #             if len(input) == 0:
# # #                 return []
# # #             input = input[0]

# # #         return self.model.encode(
# # #             [str(input)],
# # #             show_progress_bar=False,
# # #             convert_to_numpy=True
# # #         )[0].tolist()

# # #     def name(self):
# # #         return "sentence-transformers-all-MiniLM-L6-v2"

# # # _embedding_function = SentenceTransformerEmbeddingFunction(_embedding_model)

# # # # =========================
# # # # SINGLE PERSISTENT CHROMA CLIENT
# # # # =========================
# # # _client = chromadb.PersistentClient(path=CHROMA_DIR)

# # # def get_collection(name: str = COLLECTION_NAME):
# # #     """
# # #     Get or create the Chroma collection.
# # #     """
# # #     return _client.get_or_create_collection(
# # #         name=name,
# # #         embedding_function=_embedding_function
# # #     )

# # # def delete_by_source(source_name: str):
# # #     """
# # #     Delete all vectors belonging to a source.
# # #     """
# # #     collection = get_collection()
# # #     collection.delete(where={"source": source_name})
# # #     print(f"🗑️ Deleted knowledge for source: {source_name}")
# # import os
# # from pathlib import Path
# # import chromadb
# # from sentence_transformers import SentenceTransformer

# # # =========================
# # # CONFIG
# # # =========================
# # CHROMA_DIR = os.getenv("CHROMA_DB_PATH", "vectorstore")
# # COLLECTION_NAME = "sciqus_knowledge_v2"

# # os.makedirs(CHROMA_DIR, exist_ok=True)

# # # =========================
# # # EMBEDDING MODEL
# # # =========================
# # MODEL_NAME = "all-MiniLM-L6-v2"

# # HF_HOME = os.getenv("HF_HOME")
# # DOCKER_MODEL_PATH = (
# #     Path(HF_HOME)
# #     / "huggingface"
# #     / "hub"
# #     / "models--sentence-transformers--all-MiniLM-L6-v2"
# #     if HF_HOME else None
# # )

# # def load_embedding_model():
# #     if DOCKER_MODEL_PATH and DOCKER_MODEL_PATH.exists():
# #         return SentenceTransformer(str(DOCKER_MODEL_PATH), device="cpu")

# #     if os.getenv("ENV") != "production":
# #         return SentenceTransformer(MODEL_NAME, device="cpu")

# #     raise RuntimeError("❌ Embedding model unavailable in production")

# # _embedding_model = load_embedding_model()

# # # =========================
# # # CHROMA EMBEDDING FUNCTION
# # # =========================
# # class SentenceTransformerEmbeddingFunction:
# #     def __init__(self, model: SentenceTransformer):
# #         self.model = model

# #     def __call__(self, input):
# #         return self.embed_documents(input)

# #     def embed_documents(self, input):
# #         if not input:
# #             return []

# #         return self.model.encode(
# #             list(input),
# #             show_progress_bar=False,
# #             convert_to_numpy=True
# #         ).tolist()

# #     def embed_query(self, input):
# #         if isinstance(input, list):
# #             input = input[0] if input else ""

# #         return self.model.encode(
# #             [str(input)],
# #             show_progress_bar=False,
# #             convert_to_numpy=True
# #         )[0].tolist()

# #     def name(self):
# #         return "sentence-transformers-all-MiniLM-L6-v2"

# # _embedding_function = SentenceTransformerEmbeddingFunction(_embedding_model)

# # # =========================
# # # CHROMA CLIENT
# # # =========================
# # _client = chromadb.PersistentClient(path=CHROMA_DIR)

# # def get_collection(name: str = COLLECTION_NAME):
# #     return _client.get_or_create_collection(
# #         name=name,
# #         embedding_function=_embedding_function
# #     )

# # def delete_by_source(source_name: str):
# #     collection = get_collection()
# #     collection.delete(where={"source": source_name})
# #     print(f"🗑️ Deleted vectors for source: {source_name}")
# import os
# import chromadb
# from chromadb.utils import embedding_functions

# # =========================
# # CONFIG
# # =========================
# CHROMA_DIR = os.getenv("CHROMA_DB_PATH", "vectorstore")
# COLLECTION_NAME = "sciqus_knowledge_v2"

# os.makedirs(CHROMA_DIR, exist_ok=True)

# # =========================
# # OFFICIAL CHROMA EMBEDDING FUNCTION
# # =========================
# embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
#     model_name="all-MiniLM-L6-v2"
# )

# # =========================
# # CHROMA CLIENT
# # =========================
# _client = chromadb.PersistentClient(path=CHROMA_DIR)

# def get_collection(name: str = COLLECTION_NAME):
#     return _client.get_or_create_collection(
#         name=name,
#         embedding_function=embedding_function
#     )

# def delete_by_source(source_name: str):
#     collection = get_collection()
#     collection.delete(where={"source": source_name})
#     print(f"🗑️ Deleted vectors for source: {source_name}")
import os
import chromadb
from chromadb.utils import embedding_functions

# =========================
# CONFIG
# =========================

# Default to mounted Docker volume path
CHROMA_DIR = os.getenv("CHROMA_DB_PATH", "data/chroma")
COLLECTION_NAME = "sciqus_knowledge_v2"

# Ensure directory exists
os.makedirs(CHROMA_DIR, exist_ok=True)

# =========================
# EMBEDDING FUNCTION
# =========================

embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# =========================
# CHROMA CLIENT
# =========================

_client = chromadb.PersistentClient(path=CHROMA_DIR)

def get_collection(name: str = COLLECTION_NAME):
    return _client.get_or_create_collection(
        name=name,
        embedding_function=embedding_function
    )

def delete_by_source(source_name: str):
    collection = get_collection()
    collection.delete(where={"source": source_name})
    print(f"🗑️ Deleted vectors for source: {source_name}")
