from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.chat import (
    router as chat_router
)

app = FastAPI(title="AI Welfare Scheme Assistant")

origins = [
    "http://localhost:5173",
    "https://ai-based-multilingual-chatbot-for-w-seven.vercel.app",
    "https://ai-based-multilingual-chatbot-for-welfare-scheme-ho7t9adbe.vercel.app",
    "https://ai-based-multilingual-chatbot-for-w-henna.vercel.app",
    "https://ai-based-multilingual-chatbot-for-welfare-scheme-hyaj3yx35.vercel.app"
    
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)

@app.get("/")
def home():

    return {
        "message": "AI Welfare Scheme Assistant Running"
    }