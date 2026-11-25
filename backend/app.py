import logging
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from starlette.requests import Request

from routes.chat import router as chat_router

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

app = FastAPI(
    title="AI Welfare Scheme Assistant",
    # Interactive docs are handy locally but are not needed publicly.
    docs_url="/docs" if os.getenv("ENABLE_DOCS", "").lower() == "true" else None,
    redoc_url=None,
    openapi_url="/openapi.json" if os.getenv("ENABLE_DOCS", "").lower() == "true" else None,
)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://ai-based-multilingual-chatbot-for-w-seven.vercel.app",
    "https://ai-based-multilingual-chatbot-for-welfare-scheme-ho7t9adbe.vercel.app",
    "https://ai-based-multilingual-chatbot-for-w-henna.vercel.app",
    "https://ai-based-multilingual-chatbot-for-welfare-scheme-hyaj3yx35.vercel.app",
]

# Extra origins without code changes: ALLOWED_ORIGINS="https://a.com,https://b.com"
origins += [
    o.strip().rstrip("/")
    for o in os.getenv("ALLOWED_ORIGINS", "").split(",")
    if o.strip()
]

app.add_middleware(GZipMiddleware, minimum_size=1000)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    # The API uses no cookies or sessions, so credentials are not needed.
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)


@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    return response


app.include_router(chat_router)


@app.get("/")
def home():
    return {"message": "AI Welfare Scheme Assistant Running"}


@app.get("/health")
def health():
    """Liveness probe for the hosting platform."""
    return {"status": "ok"}
