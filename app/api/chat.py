from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel

from app.core.qa_engine import answer_question, extract_company_name
from app.utils.lead_utils import is_business_intent, store_lead
from app.utils.mailer import notify_sciqus_owner

router = APIRouter(tags=["Chat"])


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str


@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(
    req: ChatRequest,
    background_tasks: BackgroundTasks
):
    question = req.question

    # ==================================================
    # 1️⃣ ANSWER ALWAYS COMES FIRST (USER-FACING)
    # ==================================================
    answer = answer_question(question)

    # ==================================================
    # 2️⃣ BACKGROUND SIDE EFFECTS (EMAIL, STORAGE)
    #    → RUN ONLY AFTER ANSWER EXISTS
    # ==================================================
    def background_work(answer_text: str):
        try:
            if not is_business_intent(question):
                return

            company = extract_company_name(question)

            # Store lead (safe)
            store_lead(company, question)

            # Send email AFTER answer is ready
            notify_sciqus_owner(
                company=company,
                question=question
            )

        except Exception as e:
            # ❌ Never affect chat
            print("❌ Background task error:", e)

    background_tasks.add_task(background_work, answer)

    # ==================================================
    # 3️⃣ RESPONSE IS SENT IMMEDIATELY
    # ==================================================
    return ChatResponse(answer=answer)


# # from fastapi import APIRouter, BackgroundTasks
# # from pydantic import BaseModel

# # from app.core.qa_engine import answer_question, extract_company_name
# # from app.utils.lead_utils import is_business_intent, store_lead
# # from app.utils.mailer import notify_sciqus_owner

# # router = APIRouter(tags=["Chat"])


# # class ChatRequest(BaseModel):
# #     question: str


# # class ChatResponse(BaseModel):
# #     answer: str


# # @router.post("/chat", response_model=ChatResponse)
# # def chat_endpoint(
# #     req: ChatRequest,
# #     background_tasks: BackgroundTasks
# # ):
# #     question = req.question

# #     # ✅ 1. ALWAYS answer immediately
# #     answer = answer_question(question)

# #     # ✅ 2. Lead capture in background (NON-BLOCKING)
# #     if is_business_intent(question):
# #         company = extract_company_name(question)

# #         background_tasks.add_task(store_lead, company, question)
# #         background_tasks.add_task(notify_sciqus_owner, company, question)

# #     return ChatResponse(answer=answer)

# from fastapi import APIRouter, BackgroundTasks
# from pydantic import BaseModel

# from app.core.qa_engine import answer_question, extract_company_name
# from app.utils.lead_utils import is_business_intent, store_lead
# from app.utils.mailer import notify_sciqus_owner

# router = APIRouter(tags=["Chat"])


# class ChatRequest(BaseModel):
#     question: str


# class ChatResponse(BaseModel):
#     answer: str


# @router.post("/chat", response_model=ChatResponse)
# def chat_endpoint(req: ChatRequest, background_tasks: BackgroundTasks):
#     question = req.question

#     # ✅ 1. Answer FIRST (never blocked)
#     answer = answer_question(question)

#     # ✅ 2. ONE background task only
#     def background_work():
#         try:
#             if is_business_intent(question):
#                 company = extract_company_name(question)
#                 store_lead(company, question)
#                 notify_sciqus_owner(company, question)
#         except Exception as e:
#             print("❌ Background task error:", e)

#     background_tasks.add_task(background_work)

#     # ✅ 3. Return immediately
#     return ChatResponse(answer=answer)