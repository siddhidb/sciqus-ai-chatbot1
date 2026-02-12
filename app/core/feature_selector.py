from core.groq_client import ask_llm
from app.knowledge.features import FEATURES

def select_features_for_business(business_type: str):
    feature_list = ", ".join(FEATURES.keys())

    prompt = f"""
You are a Sciqus AMS product expert.

Available Sciqus AMS features:
{feature_list}

Business type:
{business_type}

TASK:
Select ONLY the relevant features from the available list.
Do NOT invent new features.
Return result as a comma-separated list.
"""

    raw = ask_llm(context="", question=prompt)

    selected = [
        f.strip()
        for f in raw.split(",")
        if f.strip() in FEATURES
    ]

    return selected
