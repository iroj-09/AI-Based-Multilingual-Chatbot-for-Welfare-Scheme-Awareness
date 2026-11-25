"""Loading and chunking of scheme data (shared by the DB builder and tests)."""

import html
import json
import re
from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

# Scraped dataset + hand-curated additions (see data/supplementary_schemes.py).
DATA_FILES = [
    DATA_DIR / "cleaned_schemes.jsonl",
    DATA_DIR / "supplementary_schemes.jsonl",
]

# MiniLM only embeds ~256 tokens (~1000 chars), so long scheme text must be
# split or its later parts (eligibility, documents, process) are never searchable.
CHUNK_SIZE = 800
CHUNK_OVERLAP = 120


def clean_text(text: str) -> str:
    """Remove HTML tags, decode entities, normalize whitespace."""

    if not text:
        return ""

    text = html.unescape(text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def load_documents(files=None):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )

    documents = []

    for path in files or DATA_FILES:

        if not Path(path).exists():
            continue

        with open(path, "r", encoding="utf-8") as file:

            for line_number, line in enumerate(file, start=1):

                try:
                    item = json.loads(line)

                    search_text = clean_text(item.get("search_text", ""))

                    if not search_text:
                        continue

                    name = item.get("scheme_name") or ""
                    short = item.get("short_title") or ""
                    state = item.get("state") or ""
                    categories = item.get("categories") or []

                    metadata = {
                        "scheme_id": item.get("scheme_id") or "",
                        "scheme_name": name,
                        "state": state,
                        "level": item.get("level") or "",
                        "short_title": short,
                        "categories": ",".join(categories)
                        if isinstance(categories, list)
                        else "",
                    }

                    # Prefix every chunk with the scheme identity (name, acronym,
                    # state) so each chunk is findable and self-explanatory.
                    label = name
                    if short and short.lower() != name.lower():
                        label += f" [{short}]"
                    if state:
                        label += f" ({state})"

                    for chunk in splitter.split_text(search_text):
                        documents.append(
                            Document(
                                page_content=f"{label}: {chunk}",
                                metadata=metadata,
                            )
                        )

                except Exception as e:
                    print(f"Error in {Path(path).name} line {line_number}: {e}")

    return documents
