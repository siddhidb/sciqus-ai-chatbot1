from app.services.business_answer import build_business_answer

def chat(q: str):
    if "company" in q.lower() or "business" in q.lower():
        return {"answer": build_business_answer(q)}
