# import os
# import re
# import pickle
# import threading

# from app.utils.lead_utils import is_business_intent, store_lead
# from app.utils.mailer import notify_sciqus_owner

# VECTOR_DIR = "data/vector"
# INDEX_PATH = os.path.join(VECTOR_DIR, "index.faiss")
# TEXTS_PATH = os.path.join(VECTOR_DIR, "texts.pkl")

# CONTACT_URL = "https://sciqusams.com/contact/"

# PRIMARY_MODEL = "llama-3.3-70b-versatile"
# FALLBACK_MODEL = "llama-3.1-8b-instant"

# MAX_CONTEXT_CHARS = 8000
# MIN_DISTANCE_THRESHOLD = 1.2

# BRAND_CONTEXT = """
# Sciqus Infotech is a technology company focused on account management,
# customer retention, and business growth solutions.

# Sciqus AMS helps businesses manage renewals, proposals, opportunities,
# customer interactions, collaboration, and account growth.
# """

# CACHE = {}

# # =========================
# # GLOBAL SINGLETONS
# # =========================
# _index = None
# _texts = None
# _embedder = None
# _llm_client = None
# _loaded = False
# _lock = threading.Lock()


# # =========================
# # SAFE PRELOAD
# # =========================
# def preload():
#     global _index, _texts, _embedder, _llm_client, _loaded
#     with _lock:
#         if _loaded:
#             return

#         print("🔄 Loading embedding model...")
#         from sentence_transformers import SentenceTransformer
#         _embedder = SentenceTransformer("all-MiniLM-L6-v2")
#         print("✅ Embedder loaded")

#         print("🔄 Loading vector store...")
#         import faiss
#         _index = faiss.read_index(INDEX_PATH)
#         with open(TEXTS_PATH, "rb") as f:
#             _texts = pickle.load(f)
#         print("✅ Vector store loaded")

#         from groq import Groq
#         _llm_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

#         _loaded = True


# # =========================
# # HELPERS
# # =========================
# def extract_company_name(question: str):
#     m = re.search(r"(i am owner of|i own|my company is)\s+(.*)", question.lower())
#     return m.group(2).title() if m else "Unknown Company"


# def is_sciqus_related(question: str):
#     return any(k in question.lower() for k in [
#         "sciqus", "ams", "account", "software", "services"
#     ])


# # =========================
# # MAIN ENTRY
# # =========================
# def answer_question(question: str, top_k: int = 5) -> str:
#     if not question.strip():
#         return "Please ask a question related to Sciqus AMS."

#     q_clean = question.lower()
#     if q_clean in CACHE:
#         return CACHE[q_clean]

#     if not is_sciqus_related(question):
#         return f"I help only with Sciqus AMS.\n\nContact: {CONTACT_URL}"

#     # 🔔 Lead capture (NON-BLOCKING)
#     if is_business_intent(question):
#         try:
#             store_lead(extract_company_name(question), question)
#             notify_sciqus_owner(extract_company_name(question), question)
#         except Exception as e:
#             print("⚠️ Lead capture error:", e)

#     # 🔥 Ensure models are ready BEFORE search
#     try:
#         preload()
#     except Exception:
#         return (
#             "Sciqus AMS helps IT & SaaS companies manage renewals, proposals, "
#             "and long-term customer growth.\n\n"
#             f"Contact us here:\n{CONTACT_URL}"
#         )

#     # 🔍 Vector search
#     try:
#         q_emb = _embedder.encode([question])
#         distances, indices = _index.search(q_emb, top_k)

#         chunks = [
#             _texts[i]
#             for i, d in zip(indices[0], distances[0])
#             if d < MIN_DISTANCE_THRESHOLD
#         ]

#         if not chunks:
#             return (
#                 "Sciqus AMS helps companies like yours manage accounts, renewals, "
#                 "and customer growth.\n\n"
#                 f"Learn more:\n{CONTACT_URL}"
#             )

#         context = (BRAND_CONTEXT + "\n\n" + "\n\n".join(chunks))[:MAX_CONTEXT_CHARS]

#         response = _llm_client.chat.completions.create(
#             model=PRIMARY_MODEL,
#             messages=[{"role": "user", "content": f"Context:\n{context}\n\nQ:{question}"}],
#             temperature=0,
#         )

#         answer = response.choices[0].message.content.strip()
#         CACHE[q_clean] = answer
#         return answer

#     except Exception as e:
#         print("⚠️ QA fallback:", e)
#         return (
#             "Sciqus AMS supports IT companies with account management, renewals, "
#             "and growth strategies.\n\n"
#             f"Contact us:\n{CONTACT_URL}"
#         )
import os
import re
import pickle
import faiss
from sentence_transformers import SentenceTransformer
from groq import Groq

from app.utils.lead_utils import is_business_intent, store_lead
from app.utils.mailer import notify_sciqus_owner

# =====================================================
# CONFIG
# =====================================================
VECTOR_DIR = "data/vector"
INDEX_PATH = os.path.join(VECTOR_DIR, "index.faiss")
TEXTS_PATH = os.path.join(VECTOR_DIR, "texts.pkl")
CONTACT_URL = "https://sciqusams.com/contact/"

PRIMARY_MODEL = "llama-3.3-70b-versatile"
MAX_CONTEXT_CHARS = 8000
MIN_DISTANCE_THRESHOLD = 1.2

# =====================================================
# BRAND CONTEXT
# =====================================================
BRAND_CONTEXT = """
Sciqus Infotech is a technology company focused on account management,
customer retention, and business growth solutions.

Sciqus AMS (Account Management Software) is the flagship product of
Sciqus Infotech.
"""


# =====================================================
# GLOBAL SINGLETONS (CRITICAL FIX)
# =====================================================
print("🔄 Loading embedding model...")
EMBEDDER = SentenceTransformer("all-MiniLM-L6-v2")
print("✅ Embedder loaded")

print("🔄 Loading vector store...")
INDEX = faiss.read_index(INDEX_PATH)
with open(TEXTS_PATH, "rb") as f:
    TEXTS = pickle.load(f)
print("✅ Vector store loaded")

LLM_CLIENT = Groq(api_key=os.getenv("GROQ_API_KEY"))

CACHE = {}





SCIQUES_GREETING_RESPONSE = (
    "Hi 👋<br/><br/>"
    "Sciqus works with IT and service companies to manage renewals, proposals, "
    "customer relationships, and long-term growth using <b>Sciqus AMS</b>.<br/><br/>"
    "Contact us here: https://sciqusams.com/contact/"
)

SCIQUES_OUT_OF_SCOPE_RESPONSE = (
    "I can help only with <b>Sciqus AMS</b>–related questions.<br/><br/>"
    "For business inquiries, please contact us here: "
    "https://sciqusams.com/contact/"
)
# =====================================================
# HELPERS
# =====================================================
def is_greeting(question: str) -> bool:
    greetings = [
        "hi",
        "hello",
        "hey",
        "good morning",
        "good afternoon",
        "good evening"
    ]
    q = question.lower().strip()
    return q in greetings or q.startswith(tuple(greetings))


def is_sciqus_related(question: str) -> bool:
    keywords = [
        "sciqus",
        "sciqus ams",
        "ams",
        "account management",
        "renewal",
        "proposal",
        "customer",
        "contract",
        "pricing",
        "license",
        "you",
        "ticketing",
        "vendor portals",
        "AI"
    ]
    q = question.lower()
    return any(k in q for k in keywords)

def extract_company_name(question: str):
    match = re.search(r"(i am owner of|i own|my company is|we are)\s+(.*)", question.lower())
    return match.group(2).title() if match else "Unknown Company"


def is_sciqus_related(question: str) -> bool:
    q = question.lower()
    return any(k in q for k in ["sciqus", "ams", "account management", "software"])


def business_fallback():
    return (
        "Sciqus works with IT and service companies to manage renewals, proposals, "
        "customer relationships, and long-term growth using Sciqus AMS.\n\n"
        f"Contact us here:\n{CONTACT_URL}"
    )

# =====================================================
# MAIN
# =====================================================
def answer_question(question: str, top_k: int = 10) -> str:
    q_clean = question.strip().lower()

    # =========================
    # 1️⃣ CACHE
    # =========================
    if q_clean in CACHE:
        return CACHE[q_clean]

    # =========================
    # 2️⃣ GREETING HANDLING
    # =========================
    if is_greeting(q_clean):
        return (
            "Hi 👋<br/><br/>"
            "Sciqus works with IT and service companies to manage renewals, "
            "proposals, customer relationships, and long-term growth using "
            "<b>Sciqus AMS</b>.<br/><br/>"
            "Contact us here: https://sciqusams.com/contact/"
        )

    # =========================
    # 3️⃣ OUT-OF-SCOPE GUARD
    # =========================
    if not is_sciqus_related(question):
        return (
            "I can help only with <b>Sciqus AMS</b>–related questions.<br/><br/>"
            "For business inquiries, please contact us here: "
            "https://sciqusams.com/contact/"
        )

    # =========================
    # 4️⃣ VECTOR SEARCH (SCIQUES ONLY)
    # =========================
    embedding = EMBEDDER.encode([question])
    distances, indices = INDEX.search(embedding, top_k)

    context_chunks = [
        TEXTS[i]
        for i, d in zip(indices[0], distances[0])
        if d < MIN_DISTANCE_THRESHOLD
    ]

    if not context_chunks:
        return (
            "I can help only with <b>Sciqus AMS</b>–related questions.<br/><br/>"
            "Please contact us here: https://sciqusams.com/contact/"
        )

    context = (
        BRAND_CONTEXT + "\n\n" + "\n\n".join(context_chunks)
    )[:MAX_CONTEXT_CHARS]

    prompt = f"""
Answer ONLY from the context.
If the answer is not in the context, say you can only help with Sciqus AMS.

Context:
{context}

Question:
{question}
"""

    response = LLM_CLIENT.chat.completions.create(
        model=PRIMARY_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    answer = response.choices[0].message.content.strip()

    # =========================
    # 5️⃣ CACHE RESULT
    # =========================
    CACHE[q_clean] = answer
    return answer