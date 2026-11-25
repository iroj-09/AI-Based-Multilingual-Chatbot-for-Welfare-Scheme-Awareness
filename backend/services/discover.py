"""Find more schemes, from the WHOLE database, that match a user's profile.

The curated catalogue (services/catalogue.py) is rule-checked. This module
widens the shortlist using hybrid search over all schemes, restricted to central
schemes plus the user's own state. These results are NOT checked against
eligibility rules, and the user is told so.
"""

from services import catalogue

# Canonical states and UTs (spellings match the scheme database).
STATES = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa",
    "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala",
    "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland",
    "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura",
    "Uttar Pradesh", "Uttarakhand", "West Bengal",
    "Andaman and Nicobar Islands", "Chandigarh",
    "Dadra & Nagar Haveli and Daman & Diu", "Delhi", "Jammu and Kashmir", "Ladakh",
    "Lakshadweep", "Puducherry",
]

_OCCUPATION_WORDS = {
    "farmer": "farmer agriculture cultivator crop",
    "labour": "unorganised worker labour employment wages",
    "homemaker": "women household",
    "student": "student education scholarship",
}


def build_query(profile: dict) -> str:
    """Turn quiz answers into a search query."""
    parts = [_OCCUPATION_WORDS.get(profile.get("occupation"), "")]
    if profile.get("gender") == "female":
        parts.append("women")
    age = profile.get("age", 0)
    if age >= 60:
        parts.append("senior citizen old age pension")
    elif 0 < age <= 25:
        parts.append("youth skill")
    if profile.get("income") == "low":
        parts.append("poor low income below poverty line")
    family = profile.get("family")
    if family in ("nohouse", "both"):
        parts.append("housing")
    if family in ("daughter", "both"):
        parts.append("girl child")
    parts.append("scheme benefit eligibility")
    return " ".join(p for p in parts if p)


def more_schemes(profile: dict, state_name: str, exclude: set, limit: int = 5, search_fn=None):
    """data_ids of up to `limit` further schemes: central + the user's state."""
    if search_fn is None:
        from services.rag import retrieve as search_fn  # lazy: heavy imports

    chunks = search_fn(build_query(profile), 120)

    picked = []
    for chunk in chunks:
        sid = chunk.metadata.get("scheme_id")
        if not sid or sid in exclude or sid in picked or not catalogue.exists(sid):
            continue
        chunk_state = chunk.metadata.get("state") or ""
        # Central schemes (no state) or schemes of the user's own state only.
        if chunk_state and chunk_state != state_name:
            continue
        picked.append(sid)
        if len(picked) >= limit:
            break
    return picked
