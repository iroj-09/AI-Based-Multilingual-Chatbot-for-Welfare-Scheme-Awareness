from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

VECTOR_DB_PATH = BASE_DIR / "vector_db"
JSONL_PATH = BASE_DIR / "data" / "cleaned_schemes.jsonl"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
GEMINI_MODEL = "gemini-2.5-flash"

# Simple per-IP rate limit for /chat
RATE_LIMIT_REQUESTS = 20
RATE_LIMIT_WINDOW_SECONDS = 60

MAX_QUESTION_LENGTH = 1000
