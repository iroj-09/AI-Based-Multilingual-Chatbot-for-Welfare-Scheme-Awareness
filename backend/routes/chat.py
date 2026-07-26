from fastapi import APIRouter
from pydantic import BaseModel

from services.rag import ask_rag

router = APIRouter()


class ChatRequest(BaseModel):
    question: str


@router.post("/chat")
def chat(req: ChatRequest):

    answer = ask_rag(
        req.question
    )

    return {
        "answer": answer
    }