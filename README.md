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
    "question": "Tell me about PM-KISAN"
}
```

### Response

```json
{
    "answer": "PM-KISAN is a Central Sector Scheme..."
}
```

`/chat` is rate limited per IP (see `backend/config.py`).

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

## Backend

Create a `.env` file inside the backend directory.

```env
GOOGLE_API_KEY=YOUR_GEMINI_API_KEY
```

## Frontend

```env
VITE_API_URL=http://127.0.0.1:8000
```

For production:

```env
VITE_API_URL=https://your-railway-backend.up.railway.app
```

---

# 🚀 Deployment

| Service | Platform |
|----------|----------|
| Frontend | Vercel |
| Backend | Railway |
| AI Model | Google Gemini |
| Vector Database | ChromaDB |

---


# 🎯 Future Improvements

- ✅ Eligibility Checker
- ✅ Source Citations
- ✅ Conversation Memory
- ✅ Streaming AI Responses
- ✅ Voice Support
- ✅ WhatsApp Integration
- ✅ Authentication
- ✅ Chat History
- ✅ Advanced Multilingual Support

---


# 👨‍💻 Author

**Praveen Roj**

---

## ⭐ If you found this project helpful, please consider giving it a star!
