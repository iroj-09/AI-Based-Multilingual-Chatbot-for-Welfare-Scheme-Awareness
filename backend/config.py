import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent

# Load backend/.env before any setting below reads the environment.
load_dotenv(BASE_DIR / ".env")

VECTOR_DB_PATH = BASE_DIR / "vector_db"
JSONL_PATH = BASE_DIR / "data" / "cleaned_schemes.jsonl"

# Multilingual (100+ languages incl. Hindi and other Indian languages), 8192-token
# context. Changing this requires rebuilding vector_db (see services/embeddings.py).
# Lighter alternative: intfloat/multilingual-e5-base (needs "query:"/"passage:" prefixes).
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "BAAI/bge-m3")
# Override with e.g. GEMINI_MODEL=gemini-2.5-flash-lite for higher free-tier limits.
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

# Simple per-IP rate limit for /chat
RATE_LIMIT_REQUESTS = 20
RATE_LIMIT_WINDOW_SECONDS = 60

MAX_QUESTION_LENGTH = 1000
MAX_HISTORY_TURNS = 6  # messages (not pairs) sent to the LLM
