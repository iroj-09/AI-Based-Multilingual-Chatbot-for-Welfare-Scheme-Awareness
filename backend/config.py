import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent

# Load backend/.env before any setting below reads the environment.
load_dotenv(BASE_DIR / ".env")

VECTOR_DB_PATH = BASE_DIR / "vector_db"
JSONL_PATH = BASE_DIR / "data" / "cleaned_schemes.jsonl"

# Multilingual embeddings (100+ languages incl. Hindi, Tamil, Bengali, Telugu, Marathi...).
# A question in any Indian language is embedded directly and matched against the
# English scheme text, so no translation step is needed before searching.
# Needs ~3 GB RAM. Changing this model requires rebuilding vector_db (see services/embeddings.py).
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "BAAI/bge-m3")
# Override with e.g. GEMINI_MODEL=gemini-2.5-flash-lite for higher free-tier limits.
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

# Simple per-IP rate limit for /chat
RATE_LIMIT_REQUESTS = 20
RATE_LIMIT_WINDOW_SECONDS = 60

MAX_QUESTION_LENGTH = 1000
MAX_HISTORY_TURNS = 6  # messages (not pairs) sent to the LLM
