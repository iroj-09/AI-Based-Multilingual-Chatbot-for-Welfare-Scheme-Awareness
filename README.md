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

The server keeps no sessions. Every reply returns a `state` object, and the client sends it back with the next message.

## `POST /chat/start`
Opening message (language choice). No LLM call.

## `POST /chat`

```json
{ "message": "मुझे मुफ्त गैस कनेक्शन चाहिए", "state": { "...": "state from the previous reply" } }
```

```json
{
  "reply": "...",
  "state": { "...": "send this back next time" },
  "options": [{ "label": "Farmer", "value": "1", "kind": "choice" }],
  "sources": [{ "scheme_name": "Pradhan Mantri Ujjwala Yojana (PMUY)", "state": "", "level": "Central" }],
  "checklist": { "filename": "pmuy-checklist.txt", "text": "...", "sms": "..." }
}
```

- Typed text is answered from the scheme database in the user's language, and the schemes used are listed in `sources`.
- Button values: `lang:<code>` picks a language, `cmd:restart|ask|list|lang` are menu actions, and numbers answer quiz questions.
- `GET /health` is the liveness check.

---

# 🧭 How it answers in any Indian language

1. All 850+ schemes are split into chunks and stored in ChromaDB using **BAAI/bge-m3**, a multilingual embedding model.
2. A question in any supported language is embedded as typed (no translation step) and matched against the English scheme text. Keyword (BM25) search is fused in, which helps scheme names and acronyms.
3. Gemini answers **only from the retrieved text**, in the user's language, and names the scheme. If the database does not contain the answer, it says so.
4. Follow-up questions ("what documents do I need?") are first rewritten into a standalone query using the conversation so far.

## Guided eligibility flow
After choosing a language, six number-based questions (work, state, age, gender, income, family) produce a shortlist: rule-checked schemes from a curated list of 10 (PM-KISAN, PMFBY, KCC, Kisan Maandhan, PM-JAY, PMUY, PMAY-G, Sukanya Samriddhi, MGNREGA, e-Shram), then more schemes from the whole database for the user's state and central schemes. Selecting a scheme shows who can apply, the documents and how to apply, with a downloadable / SMS-copyable checklist. These guided steps use no LLM calls, so they are fast and use no API quota. Fixed texts are hand-written in English and Hindi; other languages are translated by Gemini once and cached in `backend/i18n/`.

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
| `EMBEDDING_MODEL` | no | Defaults to `BAAI/bge-m3` (multilingual, needs ~3 GB RAM). Changing it requires rebuilding `vector_db` |
| `GEMINI_MODEL` | no | Defaults to `gemini-2.5-flash`. `gemini-2.5-flash-lite` has higher free-tier limits |
| `ALLOWED_ORIGINS` | no | Extra comma-separated frontend origins for CORS |
| `LOG_LEVEL` | no | Defaults to `INFO` |
| `ENABLE_DOCS` | no | Set `true` to expose `/docs` (off by default) |

## Frontend (`frontend/.env`, see `frontend/.env.example`)

```env
VITE_API_URL=http://127.0.0.1:8000
```

---

# 🚀 Deployment (demo setup)

The backend needs about 3 GB of RAM because it loads the bge-m3 embedding model, so a very small free instance may not be enough.

| Service | Platform |
|----------|----------|
| Frontend | Vercel (`frontend/vercel.json` handles routing) |
| Backend | Any Python host, e.g. Railway or Render (`backend/Procfile` is the start command) |
| AI Model | Google Gemini |
| Vector Database | ChromaDB (committed in `backend/vector_db`) |

**Backend:** set the root directory to `backend`, install `requirements.txt`, and add `GOOGLE_API_KEY` and `ALLOWED_ORIGINS=https://<your-frontend>`. Health check: `GET /health`.

**Frontend:** set `VITE_API_URL` to the backend URL in the Vercel project settings, then redeploy.

**Good to know**
- The free Gemini tier allows only 5 requests per minute for everyone combined. Under heavy use users will see "very busy, try again in a minute".
- Scheme details are for information only. Always verify on the official portals. The five schemes in `backend/data/supplementary_schemes.py` were written by hand; check them before relying on them.
- The rate limiter is in memory and resets when the server restarts.

---

# 🧪 Tests and data

- Run tests: `python -m pytest tests -c tests/pytest.ini -m "not slow"` (fast) or without `-m` to include retrieval tests (needs the embedding model and `vector_db`).
- Search is hybrid: vector similarity fused with BM25 keyword search, so exact scheme names and acronyms are found.
- Data: `backend/data/cleaned_schemes.jsonl` (scraped) plus `backend/data/supplementary_schemes.py` (hand-curated). After changing either, run `python backend/services/build_vector_db.py` and commit the rebuilt `vector_db/` with the code.

---

# 🎯 Roadmap

- ✅ Eligibility checker linked to the chatbot
- ✅ Source citations
- ✅ Conversation memory
- ✅ Hybrid (vector + keyword) retrieval
- ⬜ Streaming responses
- ✅ Multilingual embeddings (BAAI/bge-m3)
- ✅ Guided eligibility flow and document checklist
- ⬜ Voice input
- ⬜ WhatsApp integration
- ⬜ More central and state schemes in the dataset

---

# 👨‍💻 Author

**Praveen Roj**

---

## ⭐ If you found this project helpful, please consider giving it a star!
