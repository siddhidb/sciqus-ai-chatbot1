from fastapi import FastAPI
from pydantic import BaseModel
from app.core.qa_engine import answer_question

app = FastAPI()

class ChatRequest(BaseModel):
    question: str

@app.get("/")
def health():
    return {"status": "Sciqus AMS Chatbot running"}

@app.post("/chat")
def chat(req: ChatRequest):
    answer = answer_question(req.question)
    return {"answer": answer}
