import os
from groq import Groq

PRIMARY_MODEL = "llama-3.3-70b-versatile"
CONTACT_URL = "https://sciqusams.com/contact/"

_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_answer(question: str, contexts: list[str]) -> str:
    if not contexts:
        return (
            "I can help with information related to **Sciqus AMS**.\n\n"
            f"For more details, please contact us here:\n{CONTACT_URL}"
        )

    context_text = "\n\n".join(contexts)

    prompt = f"""
You are a professional Sciqus AMS assistant.

Rules:
- Answer naturally, like a product expert
- Use ONLY the provided context
- Do NOT mention FAQs or internal documents
- Do NOT guess or hallucinate
- If the context does not answer the question, say:
  "For more details, please contact us."

Context:
{context_text}

User Question:
{question}
"""

    response = _client.chat.completions.create(
        model=PRIMARY_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    answer = response.choices[0].message.content.strip()

    if len(answer) < 20:
        return (
            "I can help with information related to **Sciqus AMS**.\n\n"
            f"For more details, please contact us here:\n{CONTACT_URL}"
        )

    return answer
