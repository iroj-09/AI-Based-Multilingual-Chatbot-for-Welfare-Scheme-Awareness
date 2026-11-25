import os
from functools import lru_cache

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from config import GEMINI_MODEL

load_dotenv()


@lru_cache(maxsize=1)
def get_model() -> ChatGoogleGenerativeAI:
    """Created on first use so importing this module needs no API key."""

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("GOOGLE_API_KEY is not set")

    return ChatGoogleGenerativeAI(
        model=GEMINI_MODEL,
        google_api_key=api_key,
        timeout=30,
        max_retries=1,
    )


def generate_answer(prompt: str) -> str:
    return get_model().invoke(prompt).content


def format_history(history) -> str:
    """history: iterable of (role, content) tuples -> plain text transcript."""
    return "\n".join(
        f"{'User' if role == 'user' else 'Assistant'}: {content}"
        for role, content in history
    )


@lru_cache(maxsize=512)
def _rewrite(query: str, history: tuple) -> str:

    conversation = (
        f"Conversation so far:\n{format_history(history)}\n\n"
        if history
        else ""
    )

    prompt = f"""
You rewrite user queries for a search engine over Indian government
welfare schemes.

{conversation}Convert the latest query into ONE clear, standalone English
search query. Resolve references such as "it", "that scheme" or "what
documents do I need?" using the conversation. Keep any facts the user gave
(state, age, occupation, income, gender).
Expand scheme acronyms and nicknames into the full official scheme name and
keep the acronym too, e.g. "PM-KISAN" becomes "Pradhan Mantri Kisan Samman
Nidhi (PM-KISAN)", "PMAY" becomes "Pradhan Mantri Awas Yojana (PMAY)".

The query may be English, Hindi, Hinglish, or mixed.

Return ONLY the rewritten English query.

Latest query:
{query}
"""

    return get_model().invoke(prompt).content.strip()


def rewrite_query(query: str, history=()) -> str:
    """Translate to English and make standalone. Cached to save LLM calls."""
    return _rewrite(query, tuple(history))


def translate_json(payload: dict, language_name: str) -> dict:
    """Translate the string values of a flat/nested JSON object into a language.

    Keys, numbers, currency symbols, URLs, placeholders such as {name} and
    scheme names are kept unchanged.
    """
    import json
    import re

    prompt = f"""
Translate the VALUES of this JSON into simple, spoken {language_name} that a
person with low literacy can understand. Rules:
- Keep every key exactly the same.
- Keep numbers, the rupee sign, URLs, placeholders in curly braces such as
  {{name}} and {{link}}, and official scheme or brand names (for example
  PM-KISAN, Aadhaar, SMS, e-Shram) unchanged.
- Use a respectful tone and a neutral form that does not depend on the
  speaker's gender where the language allows it.
- Return ONLY valid JSON, no explanations and no code fences.

JSON:
{json.dumps(payload, ensure_ascii=False)}
"""

    text = get_model().invoke(prompt).content.strip()
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text)
    return json.loads(text)
