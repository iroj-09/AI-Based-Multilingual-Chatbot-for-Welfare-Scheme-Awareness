FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    HF_HOME=/app/.hf-cache

WORKDIR /app

# CPU-only torch keeps the image far smaller than the default CUDA build.
RUN pip install torch --index-url https://download.pytorch.org/whl/cpu

COPY requirements.txt .
RUN pip install -r requirements.txt

# Bake the embedding model into the image so start-up needs no download.
ARG EMBEDDING_MODEL=BAAI/bge-m3
ENV EMBEDDING_MODEL=${EMBEDDING_MODEL}
RUN python -c "import os; from sentence_transformers import SentenceTransformer; SentenceTransformer(os.environ['EMBEDDING_MODEL'])"

COPY . .

RUN useradd --create-home appuser && chown -R appuser /app
USER appuser

EXPOSE 8000

# Platforms such as Railway inject $PORT.
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT:-8000} --proxy-headers --forwarded-allow-ips='*'"]
