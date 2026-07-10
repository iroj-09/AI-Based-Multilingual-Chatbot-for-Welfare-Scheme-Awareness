from pathlib import Path

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from backend.services.gemini_service import (
    generate_answer,
    normalize_query
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

    normalized_question = normalize_query(
        question
    )
    
    docs = retriever.invoke(
        normalized_question
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

8. Generate answers in user's language whis is used in the query.
The query may be:
- English
- Hindi
- Hinglish
- Mixed Hindi and English

if the query is in Hindi then only answer in Hindi.
if the query is in Hinglish then only answer in Hinglish.
if the query is in hindi and written in english aplphabet then only answer in Hindi but written in english alphabet.

query: {question}

Context:

{context}

Question:

{normalized_question}
"""

    answer = generate_answer(
        prompt
    )

    return answer