"""
Build the Chroma vector DB from the scheme data.

Run from anywhere:  python backend/services/build_vector_db.py
"""

import gc
import shutil
import sys
from pathlib import Path

# Allow running as a plain script as well as a module.
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from langchain_chroma import Chroma  # noqa: E402

from config import EMBEDDING_MODEL, VECTOR_DB_PATH  # noqa: E402
from services.documents import load_documents  # noqa: E402
from services.embeddings import get_embeddings, write_marker  # noqa: E402


def build_vector_database():

    print("\nLoading documents...")
    documents = load_documents()
    print(f"Created {len(documents)} chunks")

    print(f"\nLoading embedding model {EMBEDDING_MODEL}...")
    embeddings = get_embeddings()

    # Build into a temp dir, then swap, so a failed build never
    # destroys the working database.
    final_path = Path(VECTOR_DB_PATH)
    tmp_path = final_path.with_name("vector_db_new")
    if tmp_path.exists():
        shutil.rmtree(tmp_path)

    print("\nCreating ChromaDB...")
    db = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=str(tmp_path),
    )

    # Release Chroma's file handles (needed on Windows before renaming).
    try:
        db._client._system.stop()
    except Exception:
        pass
    del db
    gc.collect()

    write_marker(tmp_path)

    if final_path.exists():
        shutil.rmtree(final_path)
    tmp_path.rename(final_path)

    print("\nDone.")


if __name__ == "__main__":
    build_vector_database()
