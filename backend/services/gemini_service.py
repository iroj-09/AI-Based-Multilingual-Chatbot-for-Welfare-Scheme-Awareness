import os
from functools import lru_cache

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from config import GEMINI_MODEL

load_dotenv()

model = ChatGoogleGenerativeAI(
    model=GEMINI_MODEL,
    google_api_key=os.getenv("GOOGLE_API_KEY"),
)


def generate_answer(prompt: str) -> str:
    return model.invoke(prompt).content


@lru_cache(maxsize=512)
def normalize_query(query: str) -> str:
    """Translate/normalize a query to English. Cached to save LLM calls."""

    prompt = f"""
You are a language normalization assistant.

Convert the following query into clear English.

The query may be:
- English
- Hindi
- Hinglish
- Mixed Hindi and English

Return ONLY the normalized English query.

Query:
{query}
"""

    return model.invoke(prompt).content.strip()
