import json
import html
import re
from pathlib import Path

from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma


# =====================================================
# CONFIG
# =====================================================

JSONL_PATH = Path("./data/cleaned_schemes.jsonl")
VECTOR_DB_PATH = "./vector_db"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


# =====================================================
# TEXT CLEANER
# =====================================================

def clean_text(text: str) -> str:
    """
    Remove HTML tags, decode entities,
    normalize whitespace.
    """

    if not text:
        return ""

    text = html.unescape(text)

    text = re.sub(r"<[^>]+>", " ", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# =====================================================
# LOAD JSONL
# =====================================================

def load_documents():

    documents = []

    with open(JSONL_PATH, "r", encoding="utf-8") as file:

        for line_number, line in enumerate(file, start=1):

            try:

                item = json.loads(line)

                search_text = clean_text(
                    item.get("search_text", "")
                )

                if not search_text:
                    continue

                document = Document(
                    page_content=search_text,
                    metadata={
                        "scheme_id": item.get("scheme_id", ""),
                        "scheme_name": item.get("scheme_name", ""),
                        "state": item.get("state", ""),
                        "level": item.get("level", ""),
                        "short_title": item.get("short_title", ""),
                        "categories": ",".join(
                            item.get("categories", [])
                        )
                        if isinstance(
                            item.get("categories", []),
                            list,
                        )
                        else "",
                    },
                )

                documents.append(document)

            except Exception as e:

                print(
                    f"Error at line {line_number}: {e}"
                )

    return documents


# =====================================================
# BUILD VECTOR DB
# =====================================================

def build_vector_database():

    print("\nLoading documents...")

    documents = load_documents()

    print(
        f"Loaded {len(documents)} scheme documents"
    )

    print("\nLoading embedding model...")

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    print("\nCreating ChromaDB...")

    vectordb = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=VECTOR_DB_PATH,
    )

   
    
# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":

    build_vector_database()

    
