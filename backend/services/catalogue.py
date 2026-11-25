"""The focused catalogue of 10 high-impact schemes used by the guided flow.

Eligibility rules here are a coarse first screen on the user's answers. They
only say "you may be eligible"; the authority decides. Documents and the
application steps shown to users are read from the scheme database
(data/cleaned_schemes.jsonl and data/supplementary_schemes.jsonl), never invented.
"""

import json
import re
from functools import lru_cache
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_FILES = [DATA_DIR / "cleaned_schemes.jsonl", DATA_DIR / "supplementary_schemes.jsonl"]

LOW_MID = ("low", "mid")  # household income below Rs 3 lakh a year


def _farmer(p):
    return p.get("occupation") == "farmer"


# key: short id used in translations ("s_<key>") and in the chat state.
# data_id: scheme_id in the scheme database.
SCHEMES = [
    {
        "key": "pmkisan",
        "data_id": "62a70e86f038bd8499a6aa53",
        "name": "Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)",
        "link": "https://pmkisan.gov.in",
        "check": _farmer,
    },
    {
        "key": "pmfby",
        "data_id": "63b811620d2bd718ff71b421",
        "name": "Pradhan Mantri Fasal Bima Yojana (PMFBY)",
        "link": "https://pmfby.gov.in",
        "check": _farmer,
    },
    {
        "key": "kcc",
        "data_id": "63d65d39eed73423e389f973",
        "name": "Kisan Credit Card (KCC)",
        "link": "",
        "check": _farmer,
    },
    {
        "key": "kmy",
        "data_id": "69896d8ebd88cb68aad3c472",
        "name": "Pradhan Mantri Kisan Maandhan Yojana",
        "link": "https://maandhan.in",
        "check": lambda p: _farmer(p) and 18 <= p.get("age", 0) <= 40,
    },
    {
        "key": "pmjay",
        "data_id": "supp-pmjay",
        "name": "Ayushman Bharat PM-JAY",
        "link": "https://pmjay.gov.in",
        "check": lambda p: p.get("income") in LOW_MID or p.get("age", 0) >= 70,
    },
    {
        "key": "pmuy",
        "data_id": "supp-pmuy",
        "name": "Pradhan Mantri Ujjwala Yojana (PMUY)",
        "link": "https://www.pmuy.gov.in",
        "check": lambda p: p.get("gender") == "female"
        and p.get("age", 0) >= 18
        and p.get("income") in LOW_MID,
    },
    {
        "key": "pmayg",
        "data_id": "supp-pmayg",
        "name": "Pradhan Mantri Awas Yojana - Gramin (PMAY-G)",
        "link": "https://pmayg.nic.in",
        "check": lambda p: p.get("family") in ("nohouse", "both") and p.get("income") in LOW_MID,
    },
    {
        "key": "ssy",
        "data_id": "supp-ssy",
        "name": "Sukanya Samriddhi Yojana",
        "link": "https://www.indiapost.gov.in",
        "check": lambda p: p.get("family") in ("daughter", "both"),
    },
    {
        "key": "mgnrega",
        "data_id": "supp-mgnrega",
        "name": "MGNREGA (Mahatma Gandhi National Rural Employment Guarantee Scheme)",
        "link": "https://nrega.nic.in",
        "check": lambda p: p.get("age", 0) >= 18 and p.get("occupation") in ("farmer", "labour"),
    },
    {
        "key": "eshram",
        "data_id": "supp-eshram",
        "name": "e-Shram Registration for Unorganised Workers",
        "link": "https://eshram.gov.in",
        "check": lambda p: p.get("occupation") == "labour" and 16 <= p.get("age", 0) <= 59,
    },
]

BY_KEY = {s["key"]: s for s in SCHEMES}
BY_DATA_ID = {s["data_id"]: s for s in SCHEMES}


def shortlist(profile: dict) -> list[str]:
    """data_ids of the catalogue schemes the user may be eligible for."""
    return [s["data_id"] for s in SCHEMES if s["check"](profile)]


def _lines(markdown: str, limit: int, max_len: int = 220) -> list[str]:
    """Turn a markdown list from the database into short plain-text lines."""
    out = []
    for raw in (markdown or "").splitlines():
        raw = re.sub(r"<[^>]*>?", " ", raw)  # stray HTML such as <br>
        line = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", raw)  # [text](url) -> text
        line = re.sub(r"^\s*(\d+[.)]|[-*•])\s*", "", line)  # list markers
        line = re.sub(r"[*_`#>]+", "", line).strip()
        if len(line) > 2:
            out.append(line[:max_len])
        if len(out) >= limit:
            break
    return out


@lru_cache(maxsize=1)
def _records() -> dict:
    """scheme_id -> the few fields we show, for ALL schemes in the database."""
    found = {}
    for path in DATA_FILES:
        if not path.exists():
            continue
        with open(path, encoding="utf-8") as f:
            for line in f:
                r = json.loads(line)
                sid = r.get("scheme_id")
                if not sid or not r.get("scheme_name"):
                    continue
                found[sid] = {
                    "name": r["scheme_name"].strip(),
                    "state": r.get("state") or "",
                    "level": r.get("level") or "",
                    "desc": (r.get("description") or "").strip()[:300],
                    "docs": _lines(r.get("documents_required", ""), limit=10),
                    "apply": _lines(r.get("application_process", ""), limit=5),
                    "elig": _lines(r.get("eligibility", ""), limit=5),
                }
    return found


def exists(data_id: str) -> bool:
    return data_id in _records()


def record(data_id: str) -> dict:
    """English record for any scheme in the database."""
    return _records().get(data_id, {"name": "", "state": "", "level": "", "desc": "",
                                    "docs": [], "apply": [], "elig": []})
