# # # # # # import pickle
# # # # # # import faiss
# # # # # # import os
# # # # # # from sentence_transformers import SentenceTransformer
# # # # # # from groq import Groq

# # # # # # # Paths
# # # # # # VECTOR_DIR = "data/vector"

# # # # # # # Load vector store
# # # # # # index = faiss.read_index(os.path.join(VECTOR_DIR, "index.faiss"))
# # # # # # texts = pickle.load(open(os.path.join(VECTOR_DIR, "texts.pkl"), "rb"))
# # # # # # metadata = pickle.load(open(os.path.join(VECTOR_DIR, "metadata.pkl"), "rb"))

# # # # # # # Load embedding model
# # # # # # embedder = SentenceTransformer("all-MiniLM-L6-v2")

# # # # # # # Groq client
# # # # # # client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# # # # # # def answer_question(question: str, top_k: int = 5) -> str:
# # # # # #     """
# # # # # #     Answers a question using Sciqus AMS knowledge only.
# # # # # #     """

# # # # # #     # Embed question
# # # # # #     q_embedding = embedder.encode([question])

# # # # # #     # Search vector DB
# # # # # #     distances, indices = index.search(q_embedding, top_k)

# # # # # #     # Build context
# # # # # #     context_chunks = []
# # # # # #     for i in indices[0]:
# # # # # #         if i < len(texts):
# # # # # #             context_chunks.append(texts[i])

# # # # # #     context = "\n\n".join(context_chunks)

# # # # # #     # Safety: no context found
# # # # # #     if not context.strip():
# # # # # #         return (
# # # # # #             "I don’t have verified information about this in Sciqus AMS. "
# # # # # #             "Please contact the Sciqus team for more details."
# # # # # #         )

# # # # # #     # Groq prompt (STRICT)
# # # # # #     prompt = f"""
# # # # # # You are a Sciqus AMS assistant.

# # # # # # RULES:
# # # # # # - Answer ONLY using the context provided.
# # # # # # - Do NOT use external knowledge.
# # # # # # - Do NOT guess or assume.
# # # # # # - If the answer is not clearly present, say you don’t know.

# # # # # # Context:
# # # # # # {context}

# # # # # # Question:
# # # # # # {question}
# # # # # # """

# # # # # #     response = client.chat.completions.create(
# # # # # #         model="llama-3.3-70b-versatile",
# # # # # #         messages=[{"role": "user", "content": prompt}],
# # # # # #         temperature=0
# # # # # #     )

# # # # # #     return response.choices[0].message.content.strip()

# # # # # import pickle
# # # # # import faiss
# # # # # import os
# # # # # from sentence_transformers import SentenceTransformer
# # # # # from groq import Groq

# # # # # # -----------------------
# # # # # # CONFIG
# # # # # # -----------------------
# # # # # VECTOR_DIR = "data/vector"
# # # # # CONTACT_URL = "https://sciqusams.com/contact/"

# # # # # # -----------------------
# # # # # # LOAD VECTOR STORE
# # # # # # -----------------------
# # # # # index = faiss.read_index(os.path.join(VECTOR_DIR, "index.faiss"))
# # # # # texts = pickle.load(open(os.path.join(VECTOR_DIR, "texts.pkl"), "rb"))
# # # # # metadata = pickle.load(open(os.path.join(VECTOR_DIR, "metadata.pkl"), "rb"))

# # # # # # -----------------------
# # # # # # MODELS
# # # # # # -----------------------
# # # # # embedder = SentenceTransformer("all-MiniLM-L6-v2")
# # # # # client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# # # # # # -----------------------
# # # # # # DOMAIN GUARD
# # # # # # -----------------------
# # # # # def is_sciqus_related(question: str) -> bool:
# # # # #     keywords = [
# # # # #         "sciqus",
# # # # #         "sciqus ams",
# # # # #         "sciqus infotech",
# # # # #         "ams",
# # # # #         "account management software"
# # # # #     ]
# # # # #     q = question.lower()
# # # # #     return any(k in q for k in keywords)

# # # # # # -----------------------
# # # # # # MAIN QA FUNCTION
# # # # # # -----------------------
# # # # # def answer_question(question: str, top_k: int = 10) -> str:
# # # # #     """
# # # # #     Answers Sciqus-related questions using vector search + Groq LLM.
# # # # #     Redirects to Contact page if answer is not available.
# # # # #     """

# # # # #     # 1. Empty input check
# # # # #     if not question or not question.strip():
# # # # #         return "Please ask a question related to Sciqus AMS."

# # # # #     # 2. Domain scope check
# # # # #     if not is_sciqus_related(question):
# # # # #         return (
# # # # #             "I can help only with questions related to Sciqus Infotech and Sciqus AMS.\n\n"
# # # # #             f"For other inquiries, please contact us here:\n{CONTACT_URL}"
# # # # #         )

# # # # #     # 3. Embed question
# # # # #     q_embedding = embedder.encode([question])

# # # # #     # 4. Vector search
# # # # #     distances, indices = index.search(q_embedding, top_k)

# # # # #     # 5. Build context
# # # # #     context_chunks = []
# # # # #     for i in indices[0]:
# # # # #         if i < len(texts):
# # # # #             context_chunks.append(texts[i])

# # # # #     context = "\n\n".join(context_chunks).strip()

# # # # #     # 6. No context found → redirect
# # # # #     if not context:
# # # # #         return (
# # # # #             "I couldn’t find verified information for your question.\n\n"
# # # # #             f"Please contact the Sciqus team here:\n{CONTACT_URL}"
# # # # #         )

# # # # #     # 7. LLM Prompt
# # # # #     prompt = f"""
# # # # # You are a Sciqus AMS assistant.

# # # # # STRICT RULES:
# # # # # - Answer ONLY using the provided context.
# # # # # - Do NOT use external knowledge.
# # # # # - Do NOT guess or assume.
# # # # # - If the context does not clearly answer the question,
# # # # #   say you do not have that information and suggest contacting the Sciqus team.

# # # # # Context:
# # # # # {context}

# # # # # Question:
# # # # # {question}

# # # # # Provide a clear, simple, business-friendly answer.
# # # # # """

# # # # #     response = client.chat.completions.create(
# # # # #         model="llama-3.3-70b-versatile",
# # # # #         messages=[{"role": "user", "content": prompt}],
# # # # #         temperature=0
# # # # #     )

# # # # #     answer = response.choices[0].message.content.strip()

# # # # #     # 8. Final safety fallback
# # # # #     uncertain_phrases = [
# # # # #         "i don't know",
# # # # #         "i do not know",
# # # # #         "not sure",
# # # # #         "no information",
# # # # #         "cannot find",
# # # # #         "not provided"
# # # # #     ]

# # # # #     if any(p in answer.lower() for p in uncertain_phrases):
# # # # #         return (
# # # # #             "I don’t have enough verified information to answer this question.\n\n"
# # # # #             f"You can contact the Sciqus team here:\n{CONTACT_URL}"
# # # # #         )

# # # # #     return answer


# # # # import pickle
# # # # import faiss
# # # # import os
# # # # from sentence_transformers import SentenceTransformer
# # # # from groq import Groq

# # # # # -----------------------
# # # # # SIMPLE IN-MEMORY CACHE
# # # # # -----------------------
# # # # CACHE = {}

# # # # # -----------------------
# # # # # CONFIG
# # # # # -----------------------
# # # # VECTOR_DIR = "data/vector"
# # # # CONTACT_URL = "https://sciqusams.com/contact/"

# # # # PRIMARY_MODEL = "llama-3.3-70b-versatile"
# # # # FALLBACK_MODEL = "llama-3.1-8b-instant"

# # # # MAX_CONTEXT_CHARS = 8000   # token control
# # # # MIN_DISTANCE_THRESHOLD = 1.2  # relevance guard

# # # # # -----------------------
# # # # # BRAND IDENTITY (ALWAYS AVAILABLE)
# # # # # -----------------------
# # # # BRAND_CONTEXT = """
# # # # Sciqus Infotech is a technology company focused on account management,
# # # # customer retention, and business growth solutions.

# # # # Sciqus AMS (Account Management Software) is the flagship product of
# # # # Sciqus Infotech.

# # # # Sciqus AMS helps businesses manage renewals, proposals, opportunities,
# # # # customer interactions, collaboration, and account growth.

# # # # Sciqus AMS is designed for SaaS companies, IT services companies,
# # # # and businesses managing long-term customer accounts.
# # # # """

# # # # # -----------------------
# # # # # LOAD VECTOR STORE
# # # # # -----------------------
# # # # index = faiss.read_index(os.path.join(VECTOR_DIR, "index.faiss"))
# # # # texts = pickle.load(open(os.path.join(VECTOR_DIR, "texts.pkl"), "rb"))
# # # # metadata = pickle.load(open(os.path.join(VECTOR_DIR, "metadata.pkl"), "rb"))

# # # # # -----------------------
# # # # # MODELS
# # # # # -----------------------
# # # # embedder = SentenceTransformer("all-MiniLM-L6-v2")
# # # # client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# # # # # -----------------------
# # # # # DOMAIN GUARD
# # # # # -----------------------
# # # # def is_sciqus_related(question: str) -> bool:
# # # #     keywords = [
# # # #         "sciqus",
# # # #         "sciqus ams",
# # # #         "sciqus infotech",
# # # #         "ams",
# # # #         "account management"
# # # #     ]
# # # #     q = question.lower()
# # # #     return any(k in q for k in keywords)

# # # # # -----------------------
# # # # # MAIN QA FUNCTION
# # # # # -----------------------
# # # # def answer_question(question: str, top_k: int = 10) -> str:
# # # #     """
# # # #     Answers Sciqus-related questions using vector search + Groq LLM.
# # # #     Redirects to Contact page if answer is not available.
# # # #     """

# # # #     # 1️⃣ Empty input
# # # #     if not question or not question.strip():
# # # #         return "Please ask a question related to Sciqus AMS."

# # # #     cache_key = question.strip().lower()

# # # #     # 2️⃣ CACHE HIT
# # # #     if cache_key in CACHE:
# # # #         return CACHE[cache_key]

# # # #     # 3️⃣ Domain check
# # # #     if not is_sciqus_related(question):
# # # #         answer = (
# # # #             "I can help only with questions related to Sciqus Infotech and Sciqus AMS.\n\n"
# # # #             f"Please contact us here:\n{CONTACT_URL}"
# # # #         )
# # # #         CACHE[cache_key] = answer
# # # #         return answer

# # # #     # 4️⃣ Embed question
# # # #     q_embedding = embedder.encode([question])

# # # #     # 5️⃣ Vector search
# # # #     distances, indices = index.search(q_embedding, top_k)

# # # #     # 6️⃣ Build context (with relevance guard)
# # # #     context_chunks = []
# # # #     for idx, dist in zip(indices[0], distances[0]):
# # # #         if idx < len(texts) and dist < MIN_DISTANCE_THRESHOLD:
# # # #             context_chunks.append(texts[idx])

# # # #     context = "\n\n".join(context_chunks).strip()

# # # #     # 7️⃣ Always prepend brand identity
# # # #     final_context = BRAND_CONTEXT + "\n\n" + context
# # # #     final_context = final_context[:MAX_CONTEXT_CHARS]

# # # #     # 8️⃣ No useful context
# # # #     if not context:
# # # #         answer = (
# # # #             "I don’t have verified information to answer this question.\n\n"
# # # #             f"You can contact the Sciqus team here:\n{CONTACT_URL}"
# # # #         )
# # # #         CACHE[cache_key] = answer
# # # #         return answer

# # # #     # 9️⃣ Prompt
# # # #     prompt = f"""
# # # # You are a Sciqus AMS assistant.

# # # # STRICT RULES:
# # # # - Answer ONLY using the provided context.
# # # # - Do NOT use external knowledge.
# # # # - Do NOT guess or assume.
# # # # - If the context does not clearly answer the question,
# # # #   say you do not have that information and suggest contacting Sciqus.

# # # # Context:
# # # # {final_context}

# # # # Question:
# # # # {question}

# # # # Provide a clear, simple, business-friendly answer.
# # # # """

# # # #     # 🔟 LLM call with fallback
# # # #     try:
# # # #         response = client.chat.completions.create(
# # # #             model=PRIMARY_MODEL,
# # # #             messages=[{"role": "user", "content": prompt}],
# # # #             temperature=0
# # # #         )
# # # #     except Exception:
# # # #         response = client.chat.completions.create(
# # # #             model=FALLBACK_MODEL,
# # # #             messages=[{"role": "user", "content": prompt}],
# # # #             temperature=0
# # # #         )

# # # #     answer = response.choices[0].message.content.strip()

# # # #     # 1️⃣1️⃣ Final safety filter
# # # #     uncertain_phrases = [
# # # #         "i don't know",
# # # #         "i do not know",
# # # #         "not sure",
# # # #         "no information",
# # # #         "cannot find",
# # # #         "not provided"
# # # #     ]

# # # #     if any(p in answer.lower() for p in uncertain_phrases):
# # # #         answer = (
# # # #             "I don’t have enough verified information to answer this question.\n\n"
# # # #             f"You can contact the Sciqus team here:\n{CONTACT_URL}"
# # # #         )

# # # #     # 1️⃣2️⃣ Cache answer
# # # #     CACHE[cache_key] = answer
# # # #     return answer
# # # import pickle
# # # import faiss
# # # import os
# # # from sentence_transformers import SentenceTransformer
# # # from groq import Groq

# # # from app.utils.lead_utils import is_business_intent, store_lead
# # # from app.utils.mailer import notify_sciqus_owner

# # # # -----------------------
# # # # CACHE
# # # # -----------------------
# # # CACHE = {}

# # # # -----------------------
# # # # CONFIG
# # # # -----------------------
# # # VECTOR_DIR = "data/vector"
# # # CONTACT_URL = "https://sciqusams.com/contact/"

# # # PRIMARY_MODEL = "llama-3.3-70b-versatile"
# # # FALLBACK_MODEL = "llama-3.1-8b-instant"

# # # MAX_CONTEXT_CHARS = 8000
# # # MIN_DISTANCE_THRESHOLD = 1.2

# # # # -----------------------
# # # # BRAND CONTEXT
# # # # -----------------------
# # # BRAND_CONTEXT = """
# # # Sciqus Infotech is a technology company focused on account management,
# # # customer retention, and business growth solutions.

# # # Sciqus AMS (Account Management Software) is the flagship product of
# # # Sciqus Infotech.

# # # Sciqus AMS helps businesses manage renewals, proposals, opportunities,
# # # customer interactions, collaboration, and account growth.
# # # """

# # # # -----------------------
# # # # LOAD VECTOR STORE
# # # # -----------------------
# # # index = faiss.read_index(os.path.join(VECTOR_DIR, "index.faiss"))
# # # texts = pickle.load(open(os.path.join(VECTOR_DIR, "texts.pkl"), "rb"))

# # # # -----------------------
# # # # MODELS
# # # # -----------------------
# # # embedder = SentenceTransformer("all-MiniLM-L6-v2")
# # # client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# # # # -----------------------
# # # # DOMAIN GUARD
# # # # -----------------------
# # # def is_sciqus_related(question: str) -> bool:
# # #     keywords = ["sciqus", "sciqus ams", "sciqus infotech", "ams"]
# # #     q = question.lower()
# # #     return any(k in q for k in keywords)

# # # # -----------------------
# # # # MAIN FUNCTION
# # # # -----------------------
# # # def answer_question(question: str, top_k: int = 10) -> str:

# # #     if not question.strip():
# # #         return "Please ask a question related to Sciqus AMS."

# # #     cache_key = question.lower()
# # #     if cache_key in CACHE:
# # #         return CACHE[cache_key]

# # #     if not is_sciqus_related(question):
# # #         answer = f"I can help only with Sciqus-related questions.\n\nContact us:\n{CONTACT_URL}"
# # #         CACHE[cache_key] = answer
# # #         return answer

# # #     # # 🎯 BUSINESS LEAD CAPTURE
# # #     # if is_business_intent(question):
# # #     #     company = question  # simple start
# # #     #     store_lead(company, question)
# # #     #     notify_sciqus_owner(company, question)



# # #     q_embedding = embedder.encode([question])
# # #     distances, indices = index.search(q_embedding, top_k)

# # #     context_chunks = [
# # #         texts[i] for i, d in zip(indices[0], distances[0])
# # #         if i < len(texts) and d < MIN_DISTANCE_THRESHOLD
# # #     ]

# # #     if not context_chunks:
# # #         answer = f"I don’t have verified info.\n\nContact us:\n{CONTACT_URL}"
# # #         CACHE[cache_key] = answer
# # #         return answer

# # #     context = BRAND_CONTEXT + "\n\n" + "\n\n".join(context_chunks)
# # #     context = context[:MAX_CONTEXT_CHARS]

# # #     prompt = f"""
# # # Answer ONLY from the context.
# # # If unsure, redirect to contact page.

# # # Context:
# # # {context}

# # # Question:
# # # {question}
# # # """

# # #     try:
# # #         response = client.chat.completions.create(
# # #             model=PRIMARY_MODEL,
# # #             messages=[{"role": "user", "content": prompt}],
# # #             temperature=0
# # #         )
# # #     except Exception:
# # #         response = client.chat.completions.create(
# # #             model=FALLBACK_MODEL,
# # #             messages=[{"role": "user", "content": prompt}],
# # #             temperature=0
# # #         )

# # #     answer = response.choices[0].message.content.strip()
# # #     CACHE[cache_key] = answer
# # #     return answer


# # import pickle
# # import faiss
# # import os
# # import re
# # from sentence_transformers import SentenceTransformer
# # from groq import Groq

# # from app.utils.lead_utils import is_business_intent, store_lead
# # from app.utils.mailer import notify_sciqus_owner

# # # -----------------------
# # # CACHE
# # # -----------------------
# # CACHE = {}

# # # -----------------------
# # # CONFIG
# # # -----------------------
# # VECTOR_DIR = "data/vector"
# # CONTACT_URL = "https://sciqusams.com/contact/"

# # PRIMARY_MODEL = "llama-3.3-70b-versatile"
# # FALLBACK_MODEL = "llama-3.1-8b-instant"

# # MAX_CONTEXT_CHARS = 8000
# # MIN_DISTANCE_THRESHOLD = 1.2

# # # -----------------------
# # # BRAND CONTEXT (ALWAYS INCLUDED)
# # # -----------------------
# # BRAND_CONTEXT = """
# # Sciqus Infotech is a technology company focused on account management,
# # customer retention, and business growth solutions.

# # Sciqus AMS (Account Management Software) is the flagship product of
# # Sciqus Infotech.

# # Sciqus AMS helps businesses manage renewals, proposals, opportunities,
# # customer interactions, collaboration, and account growth.

# # Sciqus AMS is designed for SaaS companies, IT services companies,
# # and businesses managing long-term customer accounts.
# # """

# # # -----------------------
# # # LOAD VECTOR STORE
# # # -----------------------
# # index = faiss.read_index(os.path.join(VECTOR_DIR, "index.faiss"))
# # texts = pickle.load(open(os.path.join(VECTOR_DIR, "texts.pkl"), "rb"))

# # # -----------------------
# # # MODELS
# # # -----------------------
# # embedder = SentenceTransformer("all-MiniLM-L6-v2")
# # client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# # # -----------------------
# # # HELPERS
# # # -----------------------
# # def extract_company_name(question: str) -> str | None:
# #     patterns = [
# #         r"i am owner of (.+)",
# #         r"i own (.+)",
# #         r"my company is (.+)",
# #         r"we are (.+)"
# #     ]
# #     q = question.lower()
# #     for p in patterns:
# #         match = re.search(p, q)
# #         if match:
# #             return match.group(1).strip().title()
# #     return None


# # def is_sciqus_related(question: str) -> bool:
# #     keywords = [
# #         "sciqus",
# #         "sciqus ams",
# #         "sciqus infotech",
# #         "ams",
# #         "account management"
# #     ]
# #     q = question.lower()
# #     return any(k in q for k in keywords)

# # # -----------------------
# # # MAIN QA FUNCTION
# # # -----------------------
# # def answer_question(question: str, top_k: int = 10) -> str:

# #     # 1️⃣ Empty input
# #     if not question or not question.strip():
# #         return "Please ask a question related to Sciqus AMS."

# #     cache_key = question.strip().lower()
# #     if cache_key in CACHE:
# #         return CACHE[cache_key]

# #     # 2️⃣ Domain guard
# #     if not is_sciqus_related(question):
# #         answer = (
# #             "I can help only with questions related to Sciqus Infotech and Sciqus AMS.\n\n"
# #             f"Please contact us here:\n{CONTACT_URL}"
# #         )
# #         CACHE[cache_key] = answer
# #         return answer

# #     # 3️⃣ Lead capture (NON-BLOCKING)
# #     if is_business_intent(question):
# #         company = extract_company_name(question) or "Unknown Company"
# #         try:
# #             store_lead(company, question)
# #             notify_sciqus_owner(company, question)
# #         except Exception as e:
# #             print("⚠️ Lead notification failed:", e)

# #     # 4️⃣ Embed + Vector Search
# #     q_embedding = embedder.encode([question])
# #     distances, indices = index.search(q_embedding, top_k)

# #     context_chunks = [
# #         texts[i] for i, d in zip(indices[0], distances[0])
# #         if i < len(texts) and d < MIN_DISTANCE_THRESHOLD
# #     ]

# #     # 5️⃣ No context found
# #     if not context_chunks:
# #         answer = (
# #             "I don’t have verified information to answer this question.\n\n"
# #             f"You can contact the Sciqus team here:\n{CONTACT_URL}"
# #         )
# #         CACHE[cache_key] = answer
# #         return answer

# #     # 6️⃣ Build final context
# #     context = BRAND_CONTEXT + "\n\n" + "\n\n".join(context_chunks)
# #     context = context[:MAX_CONTEXT_CHARS]

# #     # 7️⃣ Strong hallucination-safe prompt
# #     prompt = f"""
# # You are a Sciqus AMS assistant.

# # STRICT RULES:
# # - Answer ONLY using the context below
# # - Do NOT use external knowledge
# # - Do NOT guess or assume
# # - If the answer is not clearly present, say you don’t know
# #   and redirect to the contact page

# # Context:
# # {context}

# # Question:
# # {question}

# # Provide a clear, business-friendly answer.
# # """

# #     # 8️⃣ LLM call with fallback
# #     try:
# #         response = client.chat.completions.create(
# #             model=PRIMARY_MODEL,
# #             messages=[{"role": "user", "content": prompt}],
# #             temperature=0
# #         )
# #     except Exception:
# #         response = client.chat.completions.create(
# #             model=FALLBACK_MODEL,
# #             messages=[{"role": "user", "content": prompt}],
# #             temperature=0
# #         )

# #     answer = response.choices[0].message.content.strip()

# #     # 9️⃣ Final safety net
# #     uncertain_phrases = [
# #         "i don't know",
# #         "i do not know",
# #         "not sure",
# #         "no information",
# #         "cannot find",
# #         "not provided"
# #     ]

# #     if any(p in answer.lower() for p in uncertain_phrases):
# #         answer = (
# #             "I don’t have enough verified information to answer this question.\n\n"
# #             f"You can contact the Sciqus team here:\n{CONTACT_URL}"
# #         )

# #     CACHE[cache_key] = answer
# #     return answer

# import pickle
# import faiss
# import os
# import re
# from sentence_transformers import SentenceTransformer
# from groq import Groq

# from app.utils.lead_utils import is_business_intent, store_lead
# from app.utils.mailer import notify_sciqus_owner

# # -----------------------
# # CACHE
# # -----------------------
# CACHE = {}

# # -----------------------
# # CONFIG
# # -----------------------
# VECTOR_DIR = "data/vector"
# CONTACT_URL = "https://sciqusams.com/contact/"

# PRIMARY_MODEL = "llama-3.3-70b-versatile"
# FALLBACK_MODEL = "llama-3.1-8b-instant"

# MAX_CONTEXT_CHARS = 8000
# MIN_DISTANCE_THRESHOLD = 1.2

# # -----------------------
# # BRAND CONTEXT (ALWAYS INCLUDED)
# # -----------------------
# BRAND_CONTEXT = """
# Sciqus Infotech is a technology company focused on account management,
# customer retention, and business growth solutions.

# Sciqus AMS (Account Management Software) is the flagship product of
# Sciqus Infotech.

# Sciqus AMS helps businesses manage renewals, proposals, opportunities,
# customer interactions, collaboration, and account growth.

# Sciqus AMS is designed for SaaS companies, IT services companies,
# and businesses managing long-term customer accounts.
# """

# # -----------------------
# # BUSINESS FALLBACK (SALES ANSWER)
# # -----------------------
# def business_fallback_answer() -> str:
#     return (
#         "Sciqus works with service providers and businesses to help them "
#         "manage client relationships, renewals, proposals, collaboration, "
#         "and long-term account growth using Sciqus AMS.\n\n"
#         "If you manage multiple clients or long-term customer relationships, "
#         "Sciqus AMS can help bring structure, visibility, and growth.\n\n"
#         f"For partnerships or detailed discussions, please contact us here:\n{CONTACT_URL}"
#     )

# # -----------------------
# # LOAD VECTOR STORE
# # -----------------------
# index = faiss.read_index(os.path.join(VECTOR_DIR, "index.faiss"))
# texts = pickle.load(open(os.path.join(VECTOR_DIR, "texts.pkl"), "rb"))

# # -----------------------
# # MODELS
# # -----------------------
# embedder = SentenceTransformer("all-MiniLM-L6-v2")
# client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# # -----------------------
# # HELPERS
# # -----------------------
# def extract_company_name(question: str) -> str | None:
#     patterns = [
#         r"i am owner of (.+)",
#         r"i own (.+)",
#         r"my company is (.+)",
#         r"we are (.+)"
#     ]
#     q = question.lower()
#     for p in patterns:
#         match = re.search(p, q)
#         if match:
#             return match.group(1).strip().title()
#     return None


# def is_sciqus_related(question: str) -> bool:
#     q = question.lower()

#     brand_keywords = [
#         "sciqus",
#         "sciqus ams",
#         "sciqus infotech",
#         "ams",
#         "account management"
#     ]

#     business_keywords = [
#         "partner",
#         "services",
#         "help",
#         "support",
#         "solution",
#         "software",
#         "work with",
#         "collaborate"
#     ]

#     return any(k in q for k in brand_keywords) or any(k in q for k in business_keywords)

# # -----------------------
# # MAIN QA FUNCTION
# # -----------------------
# def answer_question(question: str, top_k: int = 10) -> str:

#     # 1️⃣ Empty input
#     if not question or not question.strip():
#         return "Please ask a question related to Sciqus AMS."

#     cache_key = question.strip().lower()
#     if cache_key in CACHE:
#         return CACHE[cache_key]

#     # 2️⃣ Domain guard
#     if not is_sciqus_related(question):
#         answer = (
#             "I can help only with questions related to Sciqus Infotech and Sciqus AMS.\n\n"
#             f"Please contact us here:\n{CONTACT_URL}"
#         )
#         CACHE[cache_key] = answer
#         return answer

#     # 3️⃣ Lead capture (NON-BLOCKING)
#     if is_business_intent(question):
#         company = extract_company_name(question) or "Unknown Company"
#         try:
#             store_lead(company, question)
#             notify_sciqus_owner(company, question)
#         except Exception as e:
#             print("⚠️ Lead notification failed:", e)

#     # 4️⃣ Vector search
#     q_embedding = embedder.encode([question])
#     distances, indices = index.search(q_embedding, top_k)

#     context_chunks = [
#         texts[i] for i, d in zip(indices[0], distances[0])
#         if i < len(texts) and d < MIN_DISTANCE_THRESHOLD
#     ]

#     # 5️⃣ Business intent but no exact content → SALES FALLBACK ✅
#     if not context_chunks:
#         if is_business_intent(question):
#             answer = business_fallback_answer()
#         else:
#             answer = (
#                 "I don’t have verified information to answer this question.\n\n"
#                 f"You can contact the Sciqus team here:\n{CONTACT_URL}"
#             )

#         CACHE[cache_key] = answer
#         return answer

#     # 6️⃣ Build final context
#     context = BRAND_CONTEXT + "\n\n" + "\n\n".join(context_chunks)
#     context = context[:MAX_CONTEXT_CHARS]

#     # 7️⃣ Hallucination-safe prompt
#     prompt = f"""
# You are a Sciqus AMS assistant.

# STRICT RULES:
# - Answer ONLY using the context below
# - Do NOT use external knowledge
# - Do NOT guess or assume
# - If the answer is not clearly present, say you don’t know
#   and redirect to the contact page

# Context:
# {context}

# Question:
# {question}

# Provide a clear, business-friendly answer.
# """

#     # 8️⃣ LLM call with fallback
#     try:
#         response = client.chat.completions.create(
#             model=PRIMARY_MODEL,
#             messages=[{"role": "user", "content": prompt}],
#             temperature=0
#         )
#     except Exception:
#         response = client.chat.completions.create(
#             model=FALLBACK_MODEL,
#             messages=[{"role": "user", "content": prompt}],
#             temperature=0
#         )

#     answer = response.choices[0].message.content.strip()

#     # 9️⃣ Final safety net
#     uncertain_phrases = [
#         "i don't know",
#         "i do not know",
#         "not sure",
#         "no information",
#         "cannot find",
#         "not provided"
#     ]

#     if any(p in answer.lower() for p in uncertain_phrases):
#         answer = (
#             "I don’t have enough verified information to answer this question.\n\n"
#             f"You can contact the Sciqus team here:\n{CONTACT_URL}"
#         )

#     CACHE[cache_key] = answer
#     return answer
import pickle
import faiss
import os
import re
from sentence_transformers import SentenceTransformer
from groq import Groq

from app.utils.lead_utils import is_business_intent, store_lead
from app.utils.mailer import notify_sciqus_owner

# -----------------------
# CACHE
# -----------------------
CACHE = {}

# -----------------------
# CONFIG
# -----------------------
VECTOR_DIR = "data/vector"
CONTACT_URL = "https://sciqusams.com/contact/"

PRIMARY_MODEL = "llama-3.3-70b-versatile"
FALLBACK_MODEL = "llama-3.1-8b-instant"

MAX_CONTEXT_CHARS = 8000
MIN_DISTANCE_THRESHOLD = 1.2

# -----------------------
# BRAND CONTEXT (ALWAYS INCLUDED)
# -----------------------
BRAND_CONTEXT = """
Sciqus Infotech is a technology company focused on account management,
customer retention, and business growth solutions.

Sciqus AMS (Account Management Software) is the flagship product of
Sciqus Infotech.

Sciqus AMS helps businesses manage renewals, proposals, opportunities,
customer interactions, collaboration, and account growth.

Sciqus AMS is designed for SaaS companies, IT services companies,
and businesses managing long-term customer accounts.
"""

# -----------------------
# BUSINESS FALLBACK (SALES ANSWER)
# -----------------------
def business_fallback_answer() -> str:
    return (
        "Sciqus works with service providers and businesses to help them manage "
        "client relationships, renewals, proposals, collaboration, and long-term "
        "account growth using Sciqus AMS.\n\n"
        "If you work with multiple clients or manage long-term customer relationships, "
        "Sciqus AMS can help bring structure, visibility, and predictable growth.\n\n"
        f"For partnerships or detailed discussions, please contact us here:\n{CONTACT_URL}"
    )

# -----------------------
# LOAD VECTOR STORE
# -----------------------
index = faiss.read_index(os.path.join(VECTOR_DIR, "index.faiss"))
texts = pickle.load(open(os.path.join(VECTOR_DIR, "texts.pkl"), "rb"))

# -----------------------
# MODELS
# -----------------------
embedder = SentenceTransformer("all-MiniLM-L6-v2")
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# -----------------------
# HELPERS
# -----------------------
def extract_company_name(question: str) -> str | None:
    patterns = [
        r"i am owner of (.+)",
        r"i own (.+)",
        r"my company is (.+)",
        r"we are (.+)"
    ]
    q = question.lower()
    for p in patterns:
        match = re.search(p, q)
        if match:
            return match.group(1).strip().title()
    return None


def is_sciqus_related(question: str) -> bool:
    q = question.lower()

    brand_keywords = [
        "sciqus",
        "sciqus ams",
        "sciqus infotech",
        "ams",
        "account management"
    ]

    business_keywords = [
        "partner",
        "services",
        "help",
        "support",
        "solution",
        "software",
        "work with",
        "collaborate"
    ]

    return any(k in q for k in brand_keywords) or any(k in q for k in business_keywords)

# -----------------------
# MAIN QA FUNCTION
# -----------------------
def answer_question(question: str, top_k: int = 10) -> str:

    # 1️⃣ Empty input
    if not question or not question.strip():
        return "Please ask a question related to Sciqus AMS."

    cache_key = question.strip().lower()
    if cache_key in CACHE:
        return CACHE[cache_key]

    # 2️⃣ Domain guard
    if not is_sciqus_related(question):
        answer = (
            "I can help only with questions related to Sciqus Infotech and Sciqus AMS.\n\n"
            f"Please contact us here:\n{CONTACT_URL}"
        )
        CACHE[cache_key] = answer
        return answer

    # 3️⃣ Lead capture (NON-BLOCKING)
    if is_business_intent(question):
        company = extract_company_name(question) or "Unknown Company"
        try:
            store_lead(company, question)
            notify_sciqus_owner(company, question)
        except Exception as e:
            print("⚠️ Lead notification failed:", e)

    # 4️⃣ Vector search
    q_embedding = embedder.encode([question])
    distances, indices = index.search(q_embedding, top_k)

    context_chunks = [
        texts[i] for i, d in zip(indices[0], distances[0])
        if i < len(texts) and d < MIN_DISTANCE_THRESHOLD
    ]

    # 5️⃣ Business intent but no exact content → SALES FALLBACK ✅
    if not context_chunks:
        if is_business_intent(question):
            answer = business_fallback_answer()
        else:
            answer = (
                "I don’t have verified information to answer this question.\n\n"
                f"You can contact the Sciqus team here:\n{CONTACT_URL}"
            )

        CACHE[cache_key] = answer
        return answer

    # 6️⃣ Build final context
    context = BRAND_CONTEXT + "\n\n" + "\n\n".join(context_chunks)
    context = context[:MAX_CONTEXT_CHARS]

    # 7️⃣ Hallucination-safe prompt
    prompt = f"""
You are a Sciqus AMS assistant.

STRICT RULES:
- Answer ONLY using the context below
- Do NOT use external knowledge
- Do NOT guess or assume
- If the answer is not clearly present, say you don’t know
  and redirect to the contact page

Context:
{context}

Question:
{question}

Provide a clear, business-friendly answer.
"""

    # 8️⃣ LLM call with fallback
    try:
        response = client.chat.completions.create(
            model=PRIMARY_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
    except Exception:
        response = client.chat.completions.create(
            model=FALLBACK_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

    answer = response.choices[0].message.content.strip()

    # 9️⃣ Final safety net
    uncertain_phrases = [
        "i don't know",
        "i do not know",
        "not sure",
        "no information",
        "cannot find",
        "not provided"
    ]

    if any(p in answer.lower() for p in uncertain_phrases):
        answer = (
            "I don’t have enough verified information to answer this question.\n\n"
            f"You can contact the Sciqus team here:\n{CONTACT_URL}"
        )

    CACHE[cache_key] = answer
    return answer
