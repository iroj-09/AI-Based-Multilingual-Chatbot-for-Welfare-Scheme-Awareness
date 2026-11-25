import logging
import time
from collections import defaultdict, deque

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field

from config import (
    MAX_QUESTION_LENGTH,
    RATE_LIMIT_REQUESTS,
    RATE_LIMIT_WINDOW_SECONDS,
)
from services.rag import ask_rag

logger = logging.getLogger(__name__)

router = APIRouter()

_requests: dict[str, deque] = defaultdict(deque)


def _check_rate_limit(ip: str):
    now = time.monotonic()
    window = _requests[ip]

    while window and now - window[0] > RATE_LIMIT_WINDOW_SECONDS:
        window.popleft()

    if len(window) >= RATE_LIMIT_REQUESTS:
        raise HTTPException(
            status_code=429,
            detail="Too many requests. Please wait a moment.",
        )

    window.append(now)


class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=MAX_QUESTION_LENGTH)


@router.post("/chat")
def chat(req: ChatRequest, request: Request):

    forwarded = request.headers.get("x-forwarded-for")
    ip = (
        forwarded.split(",")[0].strip()
        if forwarded
        else (request.client.host if request.client else "unknown")
    )
    _check_rate_limit(ip)

    try:
        answer = ask_rag(req.question.strip())
    except Exception:
        logger.exception("ask_rag failed")
        raise HTTPException(
            status_code=503,
            detail="The assistant is temporarily unavailable. Please try again.",
        )

    return {"answer": answer}
