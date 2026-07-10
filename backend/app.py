from fastapi import FastAPI
from backend.routes.chat import (
    router as chat_router
)

app = FastAPI(title="AI Welfare Scheme Assistant")

app.include_router(chat_router)

@app.get("/")
def home():

    return {
        "message": "AI Welfare Scheme Assistant Running"
    }