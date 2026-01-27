import json
import os
from datetime import datetime

LEADS_FILE = "data/leads.json"

def is_business_intent(question: str) -> bool:
    keywords = [
        "i am owner",
        "i own",
        "my company",
        "my business",
        "we are",
        "looking for",
        "interested in",
        "how can sciqus help",
        "how can i take help",
        "want to use sciqus"
    ]
    q = question.lower()
    return any(k in q for k in keywords)


def store_lead(company: str, question: str):
    lead = {
        "company": company,
        "question": question,
        "timestamp": datetime.utcnow().isoformat()
    }

    leads = []
    if os.path.exists(LEADS_FILE):
        with open(LEADS_FILE, "r", encoding="utf-8") as f:
            leads = json.load(f)

    leads.append(lead)

    with open(LEADS_FILE, "w", encoding="utf-8") as f:
        json.dump(leads, f, indent=2)
