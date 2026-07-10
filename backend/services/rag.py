from pathlib import Path

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from backend.services.gemini_service import (
    generate_answer
)

BASE_DIR = Path(__file__).resolve().parent.parent.parent

VECTOR_DB_PATH = BASE_DIR / "vector_db"

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = Chroma(
    persist_directory=str(VECTOR_DB_PATH),
    embedding_function=embeddings
)

retriever = db.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 5,
        "fetch_k": 20
    }
)


def ask_rag(question: str):

    docs = retriever.invoke(
        question
    )

    context = "\n\n".join(
        [
            doc.page_content
            for doc in docs
        ]
    )

    prompt = f"""
You are an Indian Government Welfare
Scheme Assistant.

IMPORTANT RULES:

1. Use ONLY information from context.

2. Never invent scheme benefits.

3. Never assume eligibility.

4. If information is unavailable,
say:
"Information not available in
the database."

5. Mention scheme names clearly.

6. Mention required documents if
available.

7. Mention application process if
available.

Context:

{context}

Question:

{question}
"""

    answer = generate_answer(
        prompt
    )

    return answer