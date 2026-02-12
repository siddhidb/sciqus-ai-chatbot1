import json
import os
from datetime import datetime

# =========================================
# STORAGE PATH (SAFE & CROSS-PLATFORM)
# =========================================

BASE_DIR = os.getenv("SCIQUS_DATA_DIR") or os.path.join(os.path.abspath(os.sep), "tmp")
QUESTIONS_FILE = os.path.join(BASE_DIR, "sciqus_questions.json")


def store_question(question: str, answer: str):
    """
    Store every answered Sciqus question for analytics.
    """

    try:
        os.makedirs(BASE_DIR, exist_ok=True)

        entry = {
            "question": question,
            "answer": answer,
            "timestamp": datetime.utcnow().isoformat()
        }

        data = []

        if os.path.exists(QUESTIONS_FILE):
            with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

        data.append(entry)

        with open(QUESTIONS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print("🧠 Question + Answer stored")

    except Exception as e:
        print("❌ Question store failed:", e)
