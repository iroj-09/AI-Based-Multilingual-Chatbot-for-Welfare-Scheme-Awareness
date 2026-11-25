# 🌾 WelfareAI – AI-Based Multilingual Welfare Scheme Assistant

> **An AI-powered multilingual chatbot that helps citizens discover, understand, and check eligibility for Indian Government welfare schemes using Retrieval-Augmented Generation (RAG), Google Gemini, and ChromaDB.**

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-blue?logo=python" />
  <img src="https://img.shields.io/badge/FastAPI-0.115+-009688?logo=fastapi" />
  <img src="https://img.shields.io/badge/React-19-61DAFB?logo=react" />
  <img src="https://img.shields.io/badge/Vite-7-646CFF?logo=vite" />
  <img src="https://img.shields.io/badge/Google-Gemini-4285F4?logo=google" />
  <img src="https://img.shields.io/badge/LangChain-RAG-green" />
  <img src="https://img.shields.io/badge/ChromaDB-Vector%20Database-orange" />
</p>

---

## 📖 Overview

India has more than **950 Central and State Government welfare schemes**, yet many citizens remain unaware of the benefits they are eligible for due to fragmented information, language barriers, and complex eligibility criteria.

**WelfareAI** is an AI-powered multilingual assistant that enables users to discover government schemes through natural conversations in **English, Hindi, and Hinglish**.

Instead of relying solely on an LLM, WelfareAI uses a **Retrieval-Augmented Generation (RAG)** pipeline. Relevant scheme documents are first retrieved from a vector database and then provided as context to **Google Gemini**, ensuring responses are grounded in official scheme information.

---

## ✨ Features

- 🤖 AI-powered Government Welfare Assistant
- 🌐 Multilingual support (English, Hindi & Hinglish)
- 🔍 Semantic search using Vector Database
- 📚 Retrieval-Augmented Generation (RAG)
- 💬 Natural conversational interface
- 📄 Markdown-formatted AI responses
- ⚡ FastAPI REST API
- 🎨 Modern React UI
- ☁️ Railway deployment
- ▲ Vercel deployment
- 📱 Fully responsive design
- ⏳ Typing indicator
- 🔄 Real-time AI responses

---

# 🏗️ System Architecture

```text
                    User
                      │
                      ▼
          React Frontend (Vercel)
                      │
                 Axios API Calls
                      │
                      ▼
         FastAPI Backend (Railway)
                      │
          Query Processing Service
                      │
      ┌───────────────┴────────────────┐
      │                                │
      ▼                                ▼
 ChromaDB Vector Search          Gemini 2.5 Flash
      │                                │
      └───────────────┬────────────────┘
                      ▼
           Context-Aware AI Response
                      │
                      ▼
              React Chat Interface
```

---

# 🚀 Tech Stack

## Frontend

- React 19
- Vite
- Tailwind CSS
- React Router
- Axios
- React Markdown
- Lucide React

### Backend

- FastAPI
- Python
- LangChain
- Google Gemini API
- ChromaDB
- Pydantic
- Uvicorn

### AI Stack

- Google Gemini 2.5 Flash
- Chroma Vector Database
- LangChain
- Retrieval-Augmented Generation (RAG)

---

# 📂 Project Structure

```text
welfare-chatbot/
│
├── backend/
│   ├── routes/
│   ├── services/
│   ├── models/
│   ├── data/
|   ├── vector_db/
│   ├── app.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── assets/
│   │   └── App.jsx
│   ├── package.json
│   └── vite.config.js
│
├── README.md

```

---

# 🧠 How It Works

```text
                User Query
                     │
                     ▼
          Language Understanding
                     │
                     ▼
          Vector Similarity Search
               (ChromaDB)
                     │
                     ▼
        Top Relevant Scheme Documents
                     │
                     ▼
           Prompt Construction
                     │
                     ▼
         Google Gemini 2.5 Flash
                     │
                     ▼
      Context-Aware AI Response
                     │
                     ▼
             React Frontend
```

---

# 🔄 RAG Pipeline

```text
Government Welfare Scheme Dataset
              │
              ▼
 Data Cleaning & Preprocessing
              │
              ▼
 Document Chunking
              │
              ▼
 Embedding Generation
              │
              ▼
      ChromaDB
              │
──────── Runtime ────────
              │
          User Query
              │
              ▼
      Semantic Retrieval
              │
              ▼
     Top Relevant Documents
              │
              ▼
        Gemini 2.5 Flash
              │
              ▼
      AI Generated Response
```

---

# 💬 Chatbot Capabilities

The chatbot can answer questions like:

- What is PM-KISAN?
- Who is eligible for Ayushman Bharat?
- What documents are required for PMAY?
- Explain Ujjwala Scheme.
- Government schemes for women.
- Farmer welfare schemes.
- Scholarship schemes for students.

---

# 🌐 Supported Languages

- 🇬🇧 English
- 🇮🇳 Hindi
- 🇮🇳 Hinglish

---

# 📡 API

## Chat Endpoint

```http
POST /chat
```

### Request

```json
{
    "question": "What documents do I need?",
    "history": [
        {"role": "user", "content": "Tell me about PM-KISAN"},
        {"role": "assistant", "content": "PM-KISAN is a Central Sector Scheme..."}
    ]
}
```

`history` is optional; it lets the bot resolve follow-up questions.

### Response

```json
{
    "answer": "PM-KISAN is a Central Sector Scheme...",
    "sources": [{"scheme_name": "Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)", "state": "", "level": "Central"}]
}
```

`/chat` is rate limited per IP (see `backend/config.py`).

### Rebuilding the vector DB and running tests

```bash
cd backend
python services/build_vector_db.py        # re-chunks and re-embeds data/cleaned_schemes.jsonl
pip install -r requirements-dev.txt
cd .. && python -m pytest tests -c tests/pytest.ini
```

Set `ALLOWED_ORIGINS` (comma-separated) to allow extra frontend origins without editing code.

## Eligibility Endpoint

```http
POST /eligibility
```

```json
{
    "age": 35,
    "gender": "Female",
    "occupation": "Farmer",
    "income": 200000
}
```

Response: `{"recommended_schemes": ["PM-KISAN", "Ayushman Bharat", "Ujjwala Yojana"]}`

---

# ⚙️ Local Setup

## Clone Repository

```bash
git clone https://github.com/<your-username>/welfare-chatbot.git

cd welfare-chatbot
```

---

## Backend Setup

```bash
cd backend

python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate

pip install -r requirements.txt

uvicorn app:app --reload
```

Backend runs at:

```
http://127.0.0.1:8000
```

---

## Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

Frontend runs at:

```
http://localhost:5173
```

---

# 🔑 Environment Variables

## Backend (`backend/.env`, see `backend/.env.example`)

| Variable | Required | Purpose |
|----------|----------|---------|
| `GOOGLE_API_KEY` | yes | Gemini API key |
| `EMBEDDING_MODEL` | no | Defaults to `BAAI/bge-m3` (multilingual). Changing it requires rebuilding `vector_db` |
| `GEMINI_MODEL` | no | Defaults to `gemini-2.5-flash`. `gemini-2.5-flash-lite` has higher free-tier limits |
| `ALLOWED_ORIGINS` | no | Extra comma-separated frontend origins for CORS |
| `LOG_LEVEL` | no | Defaults to `INFO` |
| `ENABLE_DOCS` | no | Set `true` to expose `/docs` (off by default) |

## Frontend (`frontend/.env`, see `frontend/.env.example`)

```env
VITE_API_URL=http://127.0.0.1:8000
```

---

# 🚀 Deployment

| Service | Platform |
|----------|----------|
| Frontend | Vercel (`frontend/vercel.json` handles SPA routing) |
| Backend | Railway, using `backend/Dockerfile` and `backend/railway.json` |
| AI Model | Google Gemini |
| Vector Database | ChromaDB (committed in `backend/vector_db`) |

## Backend on Railway
1. Create a service from this repo and set **Root Directory** to `backend`.
2. Add variables: `GOOGLE_API_KEY` and `ALLOWED_ORIGINS=https://<your-frontend-domain>`.
3. Deploy. Railway uses the Dockerfile and checks `GET /health`.
4. The image needs roughly 3 GB of RAM because it loads the `bge-m3` embedding model (~2.2 GB download, baked into the image). For a smaller host, build with `EMBEDDING_MODEL=intfloat/multilingual-e5-base` and rebuild `vector_db` (e5 models also need `query:`/`passage:` prefixes, which this code does not add yet).

## Frontend on Vercel
1. Import the repo with **Root Directory** `frontend`.
2. Set `VITE_API_URL` to the Railway URL **in the Vercel project settings** (the local `.env` file is not used for the build).
3. Redeploy after changing the variable.

## Before going public
- **Use a paid Gemini key.** The free tier allows only 5 requests per minute for the whole project, and one chat uses up to 2 requests. Real traffic will hit that immediately and users will see "very busy".
- Review the entries in `backend/data/supplementary_schemes.py` against the official portals. Benefit amounts and rules change.
- Keep the in-app notice that answers are informational and must be verified on official sites.
- The rate limiter is in memory. If you run more than one backend instance, move it to Redis.

---

# 🧪 Quality

- `python -m pytest tests -c tests/pytest.ini -m "not slow"` runs the fast tests (used by CI in `.github/workflows/ci.yml`).
- Drop `-m "not slow"` to also run retrieval tests (needs the embedding model and `vector_db`).
- Search is hybrid: vector similarity (`BAAI/bge-m3`, multilingual) fused with BM25 keyword search, so exact scheme names and acronyms are found.
- Data: `backend/data/cleaned_schemes.jsonl` (scraped) plus `backend/data/supplementary_schemes.py` (hand-curated central schemes). After changing either, run `python backend/services/build_vector_db.py` and commit the rebuilt `vector_db/` together with the code.

---

# 🎯 Roadmap

- ✅ Eligibility checker linked to the chatbot
- ✅ Source citations
- ✅ Conversation memory
- ✅ Hybrid (vector + keyword) retrieval
- ⬜ Streaming responses
- ✅ Multilingual embedding model (BAAI/bge-m3)
- ⬜ Voice input
- ⬜ WhatsApp integration
- ⬜ More central and state schemes in the dataset

---

# 👨‍💻 Author

**Praveen Roj**

---

## ⭐ If you found this project helpful, please consider giving it a star!
