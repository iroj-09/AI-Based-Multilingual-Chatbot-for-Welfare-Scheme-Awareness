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
from services import flow

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


class ChatRequest(BaseModel):
    # Button values such as "lang:hi" or "cmd:restart" are short; typed text is capped.
    message: str = Field(min_length=1, max_length=MAX_QUESTION_LENGTH)
    # Conversation state returned by the previous reply. The server keeps no
    # sessions, and re-validates this on every request.
    state: dict | None = None


@router.post("/chat/start")
def chat_start():
    """Opening message: language choice. No LLM call."""
    return flow.start()


@router.post("/chat")
def chat(req: ChatRequest, request: Request):

    _check_rate_limit(_client_ip(request))

    try:
        return flow.handle(req.message, req.state)
    except Exception as exc:
        logger.exception("chat failed")

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
