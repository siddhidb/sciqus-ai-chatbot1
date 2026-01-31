import json
import os
from datetime import datetime

# =========================================
# SAFE, CROSS-PLATFORM LEAD STORAGE PATH
# =========================================

BASE_DIR = os.getenv("SCIQUS_DATA_DIR")

if not BASE_DIR:
    # Windows -> C:\tmp
    # Linux / Render -> /tmp
    BASE_DIR = os.path.join(os.path.abspath(os.sep), "tmp")

LEADS_FILE = os.path.join(BASE_DIR, "sciqus_leads.json")


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
        "want to use sciqus"
    ]
    q = question.lower()
    return any(k in q for k in keywords)


def store_lead(company: str, question: str):
    try:
        # ✅ ENSURE DIRECTORY EXISTS
        os.makedirs(BASE_DIR, exist_ok=True)

        lead = {
            "company": company or "Unknown",
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

        print("✅ Lead stored successfully:", LEADS_FILE)

    except Exception as e:
        print("❌ Lead storage error:", e)