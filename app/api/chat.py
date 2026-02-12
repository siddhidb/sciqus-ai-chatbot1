# from fastapi import APIRouter, BackgroundTasks
# from pydantic import BaseModel

# from app.core.retrieval import retrieve_context
# from app.core.llm import generate_answer
# from app.core.guards import (
#     is_greeting,
#     greeting_response,
#     is_sciqus_related,
#     out_of_scope_response,
# )

# from app.utils.question_store import store_question
# from app.utils.lead_utils import is_business_intent, store_lead
# from app.utils.mailer import notify_sciqus_owner

# router = APIRouter(tags=["Chat"])


# class ChatRequest(BaseModel):
#     question: str


# class ChatResponse(BaseModel):
#     answer: str


# @router.post("/chat", response_model=ChatResponse)
# def chat_endpoint(req: ChatRequest, background_tasks: BackgroundTasks):
#     question = req.question.strip()

#     # 👋 1. Greeting (NO LLM)
#     if is_greeting(question):
#         answer = greeting_response()
#         background_tasks.add_task(store_question, question, answer)
#         return ChatResponse(answer=answer)

#     # 🔒 2. Non-Sciqus guard (NO LLM)
#     if not is_sciqus_related(question):
#         answer = out_of_scope_response()
#         background_tasks.add_task(store_question, question, answer)
#         return ChatResponse(answer=answer)

#     # 🔍 3. Retrieve knowledge
#     contexts = retrieve_context(question, top_k=5)
#     if not contexts:
#         answer = out_of_scope_response()
#         background_tasks.add_task(store_question, question, answer)
#         return ChatResponse(answer=answer)

#     # 🤖 4. Generate grounded answer
#     answer = generate_answer(question, contexts)
#     background_tasks.add_task(store_question, question, answer)

#     # 💼 5. Business workflow (async, safe)
#     def business_work():
#         try:
#             if not is_business_intent(question):
#                 return

#             store_lead("Unknown Company", question)
#             notify_sciqus_owner(
#                 company="Unknown Company",
#                 question=question
#             )

#         except Exception as e:
#             print("❌ Business workflow error:", e)

#     background_tasks.add_task(business_work)

#     return ChatResponse(answer=answer)


from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel

from app.core.retrieval import retrieve_context
from app.core.llm import generate_answer
from app.core.guards import (
    is_greeting,
    greeting_response,
    is_sciqus_related,
    out_of_scope_response,
)
from app.utils.question_store import store_question
from app.utils.lead_utils import is_business_intent, store_lead
from app.utils.mailer import notify_sciqus_owner

router = APIRouter(tags=["Chat"])

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str

@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(req: ChatRequest, background_tasks: BackgroundTasks):
    question = req.question.strip()

    # 1️⃣ Greeting
    if is_greeting(question):
        answer = greeting_response()
        background_tasks.add_task(store_question, question, answer)
        return ChatResponse(answer=answer)

    # 2️⃣ Scope guard
    if not is_sciqus_related(question):
        answer = out_of_scope_response()
        background_tasks.add_task(store_question, question, answer)
        return ChatResponse(answer=answer)

    # 3️⃣ Retrieval
    contexts = retrieve_context(question)
    if not contexts:
        answer = out_of_scope_response()
        background_tasks.add_task(store_question, question, answer)
        return ChatResponse(answer=answer)

    # 4️⃣ LLM grounded answer
    answer = generate_answer(question, contexts)
    background_tasks.add_task(store_question, question, answer)

    # 5️⃣ Business workflow (async)
    def business_flow():
        try:
            if not is_business_intent(question):
                return

            store_lead("Unknown Company", question)
            notify_sciqus_owner(
                company="Unknown Company",
                question=question
            )
        except Exception as e:
            print("❌ Business workflow error:", e)

    background_tasks.add_task(business_flow)

    return ChatResponse(answer=answer)

