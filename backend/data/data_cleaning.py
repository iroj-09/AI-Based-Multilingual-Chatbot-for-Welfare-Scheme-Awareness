import json
import html

with open("./backend/data/schemes_with_documents.json", "r", encoding="utf-8") as f:
    schemes = json.load(f)

cleaned = []

def get_label(obj):
    if isinstance(obj, dict):
        return obj.get("label")
    return None

for item in schemes:

    scheme = item.get("data", {}).get("en", {})
    basic = scheme.get("basicDetails", {}) or {}
    content = scheme.get("schemeContent", {}) or {}
    eligibility = scheme.get("eligibilityCriteria", {}) or {}
    docs = item.get("documents", {}).get("data", {}).get("en", {}) or {}

    record = {
        "scheme_id": item.get("data", {}).get("_id"),

        "scheme_name": basic.get("schemeName"),
        "short_title": basic.get("schemeShortTitle"),

        "state": get_label(basic.get("state")),
        "level": get_label(basic.get("level")),

        "categories": [
            c.get("label")
            for c in (basic.get("schemeCategory") or [])
            if isinstance(c, dict)
        ],

        "tags": basic.get("tags", []),

        "description": html.unescape(
            content.get("briefDescription", "")
        ),

        "benefits": html.unescape(
            content.get("benefits_md", "")
        ),

        "eligibility": html.unescape(
            eligibility.get("eligibilityDescription_md", "")
        ),

        "application_process": html.unescape(
            (
                scheme.get("applicationProcess", [{}])[0]
                if scheme.get("applicationProcess")
                else {}
            ).get("process_md", "")
        ),

        "documents_required": html.unescape(
            docs.get("documentsRequired_md", "")
        )
    }

    record["search_text"] = f"""
Scheme Name: {record['scheme_name']}
State: {record['state']}
Description: {record['description']}
Benefits: {record['benefits']}
Eligibility: {record['eligibility']}
Documents: {record['documents_required']}
"""

    cleaned.append(record)

with open("./backend/data/cleaned_schemes.jsonl", "w", encoding="utf-8") as f:
    for record in cleaned:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")



