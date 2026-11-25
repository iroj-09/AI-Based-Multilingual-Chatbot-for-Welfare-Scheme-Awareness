"""Languages, UI strings and translation (cached on disk).

English and Hindi strings are hand-written in backend/i18n/. For every other
language the English strings are translated by Gemini once, then saved to
backend/i18n/<code>.json so later requests need no LLM call.
"""

import json
import logging
import unicodedata
from functools import lru_cache
from pathlib import Path

from services import catalogue

logger = logging.getLogger(__name__)

I18N_DIR = Path(__file__).resolve().parent.parent / "i18n"

# code -> (English name, native name)
LANGUAGES = {
    "en": ("English", "English"),
    "hi": ("Hindi", "हिन्दी"),
    "ta": ("Tamil", "தமிழ்"),
    "bn": ("Bengali", "বাংলা"),
    "te": ("Telugu", "తెలుగు"),
    "mr": ("Marathi", "मराठी"),
    "gu": ("Gujarati", "ગુજરાતી"),
    "kn": ("Kannada", "ಕನ್ನಡ"),
    "ml": ("Malayalam", "മലയാളം"),
    "pa": ("Punjabi", "ਪੰਜਾਬੀ"),
    "or": ("Odia", "ଓଡ଼ିଆ"),
    "ur": ("Urdu", "اردو"),
    "as": ("Assamese", "অসমীয়া"),
}

# Unicode block -> language, used when a user types without choosing a language.
_SCRIPTS = [
    (0x0900, 0x097F, "hi"),
    (0x0980, 0x09FF, "bn"),
    (0x0A00, 0x0A7F, "pa"),
    (0x0A80, 0x0AFF, "gu"),
    (0x0B00, 0x0B7F, "or"),
    (0x0B80, 0x0BFF, "ta"),
    (0x0C00, 0x0C7F, "te"),
    (0x0C80, 0x0CFF, "kn"),
    (0x0D00, 0x0D7F, "ml"),
    (0x0600, 0x06FF, "ur"),
]


def language_name(code: str) -> str:
    return LANGUAGES.get(code, LANGUAGES["en"])[0]


def detect_language(text: str) -> str:
    """Guess the language from the script. Roman script is treated as English."""
    for ch in text:
        cp = ord(ch)
        for lo, hi, code in _SCRIPTS:
            if lo <= cp <= hi:
                return code
    return "en"


def parse_number(text: str):
    """First integer in text. Accepts Indian-script digits (e.g. १२, ௧௨)."""
    digits = ""
    for ch in text:
        if ch.isdigit():
            digits += str(unicodedata.digit(ch, 0))
        elif digits:
            break
    return int(digits) if digits else None


def _read(path: Path):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


@lru_cache(maxsize=32)
def _strings(code: str):
    """(strings, translated_ok). Falls back to English if translation fails."""
    english = _read(I18N_DIR / "en.json")
    if code == "en":
        return english, True

    saved = _read(I18N_DIR / f"{code}.json")
    if saved:
        return {**english, **saved}, True

    try:
        from services.gemini_service import translate_json

        translated = translate_json(english, language_name(code))
        # Keep only keys we know, as strings, so a bad reply cannot break the UI.
        clean = {k: v for k, v in translated.items() if k in english and isinstance(v, str)}
        if len(clean) < len(english) * 0.8:
            raise ValueError("incomplete translation")
        (I18N_DIR / f"{code}.json").write_text(
            json.dumps(clean, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        return {**english, **clean}, True
    except Exception:
        logger.exception("UI translation to %s failed", code)
        _strings.cache_clear()  # do not cache the failure; retry next time
        return english, False


def strings(code: str) -> dict:
    return _strings(code)[0]


def translation_ok(code: str) -> bool:
    return _strings(code)[1]


def t(code: str, key: str, **fmt) -> str:
    text = strings(code).get(key) or strings("en").get(key, key)
    return text.format(**fmt) if fmt else text


# --- per-scheme details (any scheme in the database) ---------------------------

_DETAILS_CACHE = {}


def scheme_details(data_id: str, code: str):
    """Documents, application steps, eligibility and description in the user's language.

    English comes straight from the scheme database. Other languages are
    translated once per (scheme, language) and cached on disk.
    Returns {"docs", "apply", "elig", "desc", "ok"}.
    """
    english = {k: v for k, v in catalogue.record(data_id).items()
               if k in ("docs", "apply", "elig", "desc")}
    if code == "en" or not any(english.values()):
        return {**english, "ok": True}

    path = I18N_DIR / f"details_{code}.json"
    cache = _DETAILS_CACHE.setdefault(code, _read(path) or {})
    if data_id in cache:
        return {**cache[data_id], "ok": True}

    try:
        from services.gemini_service import translate_json

        result = translate_json(english, language_name(code))
        cleaned = {
            "docs": [str(x) for x in result.get("docs", [])][:10],
            "apply": [str(x) for x in result.get("apply", [])][:5],
            "elig": [str(x) for x in result.get("elig", [])][:5],
            "desc": str(result.get("desc", "")),
        }
        # A list that changed length means lines were merged or dropped: do not trust it.
        for k in ("docs", "apply", "elig"):
            if len(cleaned[k]) != len(english[k]):
                raise ValueError(f"{k} length changed in translation")
        cache[data_id] = cleaned
        path.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")
        return {**cleaned, "ok": True}
    except Exception:
        logger.exception("details translation failed for %s/%s", data_id, code)
        return {**english, "ok": False}
