from app.knowledge.features import FEATURES
from app.core.groq_client import ask_llm
import os

CONTACT = os.getenv("CONTACT_URL")

def build_answer(context, question, feature=None):
    answer = ask_llm(context, question)
    if feature:
        answer += f"\n\nLearn more: {FEATURES[feature]['url']}"
        answer += f"\nGet in touch: {CONTACT}"
    return answer
