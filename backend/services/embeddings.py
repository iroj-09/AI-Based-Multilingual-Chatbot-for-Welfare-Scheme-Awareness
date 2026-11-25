"""Embedding model setup shared by the DB builder and the runtime."""

from pathlib import Path

from langchain_huggingface import HuggingFaceEmbeddings

from config import EMBEDDING_MODEL, VECTOR_DB_PATH

# Written next to the DB so a DB built with one model is never queried with another
# (different models give incompatible vectors and silently wrong results).
MARKER_NAME = "embedding_model.txt"


def get_embeddings() -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        # Normalised vectors make distances comparable across queries.
        encode_kwargs={"normalize_embeddings": True},
    )


def write_marker(db_path: Path) -> None:
    (Path(db_path) / MARKER_NAME).write_text(EMBEDDING_MODEL, encoding="utf-8")


def check_marker(db_path: Path = VECTOR_DB_PATH) -> None:
    marker = Path(db_path) / MARKER_NAME
    built_with = marker.read_text(encoding="utf-8").strip() if marker.exists() else None

    if built_with != EMBEDDING_MODEL:
        raise RuntimeError(
            f"vector_db was built with {built_with or 'an unknown model'} but "
            f"EMBEDDING_MODEL is {EMBEDDING_MODEL}. Rebuild it with "
            "`python backend/services/build_vector_db.py`."
        )
