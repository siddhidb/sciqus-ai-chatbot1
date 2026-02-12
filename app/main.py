# app/main.py

from dotenv import load_dotenv
load_dotenv()

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.chat import router as chat_router
from app.api.admin import router as admin_router

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "..", "frontend")

app = FastAPI(
    title="Sciqus AMS Chatbot",
    version="1.0.0"
)

# --------------------
# CORS
# --------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten later if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------
# Health
# --------------------
@app.get("/")
def health():
    return {
        "status": "ok",
        "service": "Sciqus AMS Chatbot"
    }

# --------------------
# Serve UIs
# --------------------
app.mount(
    "/ui",
    StaticFiles(directory=os.path.join(FRONTEND_DIR, "user"), html=True),
    name="user-ui"
)

app.mount(
    "/admin-ui",
    StaticFiles(directory=os.path.join(FRONTEND_DIR, "admin"), html=True),
    name="admin-ui"
)

# --------------------
# APIs
# --------------------
app.include_router(chat_router)    # /chat
app.include_router(admin_router)   # /admin/*

