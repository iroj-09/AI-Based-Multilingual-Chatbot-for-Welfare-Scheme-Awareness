import logging
import time
from collections import defaultdict, deque
from typing import Literal

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field

from config import (
    MAX_HISTORY_TURNS,
    MAX_QUESTION_LENGTH,
    RATE_LIMIT_REQUESTS,
    RATE_LIMIT_WINDOW_SECONDS,
)
from services.rag import ask_rag

logger = logging.getLogger(__name__)

router = APIRouter()

_requests: dict[str, deque] = defaultdict(deque)


def _client_ip(request: Request) -> str:
    # Behind a reverse proxy (Railway etc.) the proxy appends the real client IP
    # as the LAST x-forwarded-for entry. Earlier entries can be forged by the
    # client, so they must not be trusted for rate limiting.
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[-1].strip()
    return request.client.host if request.client else "unknown"


def _check_rate_limit(ip: str):
    now = time.monotonic()

    # Drop idle clients so the dict cannot grow without bound.
    if len(_requests) > 10000:
        for key in [k for k, w in _requests.items() if not w or now - w[-1] > RATE_LIMIT_WINDOW_SECONDS]:
            del _requests[key]

    window = _requests[ip]

    while window and now - window[0] > RATE_LIMIT_WINDOW_SECONDS:
        window.popleft()

    if len(window) >= RATE_LIMIT_REQUESTS:
        raise HTTPException(
            status_code=429,
            detail="Too many requests. Please wait a moment.",
        )

    window.append(now)


class HistoryItem(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(max_length=4000)


class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=MAX_QUESTION_LENGTH)
    history: list[HistoryItem] = Field(default_factory=list, max_length=20)


@router.post("/chat")
def chat(req: ChatRequest, request: Request):

    _check_rate_limit(_client_ip(request))

    try:
        # Only the last few turns are needed to resolve follow-ups.
        history = [(h.role, h.content) for h in req.history[-MAX_HISTORY_TURNS:]]
        result = ask_rag(req.question.strip(), history)
    except Exception as exc:
        logger.exception("ask_rag failed")

        # Upstream LLM quota exhausted: tell the user to retry, not that it is broken.
        text = str(exc)
        if "RESOURCE_EXHAUSTED" in text or "429" in text:
            raise HTTPException(
                status_code=429,
                detail="The assistant is very busy right now. Please try again in a minute.",
            )

        raise HTTPException(
            status_code=503,
            detail="The assistant is temporarily unavailable. Please try again.",
        )

    return result
