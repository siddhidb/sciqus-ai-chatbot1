# app/core/qa_engine.py

from app.core.retrieval import retrieve_context
from groq import Groq
import os

CONTACT_URL = "https://sciqusams.com/contact/"
PRIMARY_MODEL = "llama-3.3-70b-versatile"
MAX_CONTEXT_CHARS = 6000

BRAND_CONTEXT = """
Sciqus Infotech provides account management and customer growth solutions.
Sciqus AMS is its flagship Account Management Software.
"""

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def answer_question(question: str) -> str:
    question = question.strip()

    # 1️⃣ Retrieve knowledge
    chunks = retrieve_context(question, top_k=5)

    if not chunks:
        return (
            "I can help only with questions related to Sciqus AMS.\n\n"
            f"Please contact us here: {CONTACT_URL}"
        )

    context = (
        BRAND_CONTEXT + "\n\n" + "\n\n".join(chunks)
    )[:MAX_CONTEXT_CHARS]

    # 2️⃣ Grounded prompt
    prompt = f"""
You are a Sciqus AMS assistant.

Answer ONLY using the information provided below.
If the answer is not found in the context, say:
"I can help only with Sciqus AMS related information."

Context:
{context}

Question:
{question}
"""

    # 3️⃣ LLM call
    response = client.chat.completions.create(
        model=PRIMARY_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    return response.choices[0].message.content.strip()
