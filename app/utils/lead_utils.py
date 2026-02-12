import json
import os
from datetime import datetime

# ===============================
# STORAGE PATH (SAFE)
# ===============================
BASE_DIR = os.getenv("SCIQUS_DATA_DIR")

if not BASE_DIR:
    BASE_DIR = os.path.join(os.path.abspath(os.sep), "tmp")

os.makedirs(BASE_DIR, exist_ok=True)

QUESTIONS_FILE = os.path.join(BASE_DIR, "sciqus_questions.json")
LEADS_FILE = os.path.join(BASE_DIR, "sciqus_leads.json")


# ===============================
# QUESTION STORAGE (ALL USERS)
# ===============================
def store_question(question: str):
    try:
        entry = {
            "question": question,
            "timestamp": datetime.utcnow().isoformat()
        }

        data = []
        if os.path.exists(QUESTIONS_FILE):
            with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

        data.append(entry)

        with open(QUESTIONS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        print("📝 Question stored")

    except Exception as e:
        print("❌ Question storage error:", e)


# ===============================
# BUSINESS INTENT DETECTION
# ===============================
def is_business_intent(question: str) -> bool:
    keywords = [
        "i am owner",
        "i own",
        "my company",
        "my business",
        "we are",
        "pricing",
        "demo",
        "interested in",
        "how can sciqus help",
        "want to use sciqus"
    ]
    q = question.lower()
    return any(k in q for k in keywords)


# ===============================
# LEAD STORAGE (ONLY SALES)
# ===============================
def store_lead(company: str, question: str):
    try:
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

        print("🚀 Lead stored")

    except Exception as e:
        print("❌ Lead storage error:", e)
