# AI Multilingual Welfare Scheme Chatbot

A RAG chatbot that answers questions about Indian government welfare schemes in
English, Hindi and Hinglish, plus a simple rule-based eligibility checker.

## Stack
- Backend: FastAPI, LangChain, ChromaDB, `all-MiniLM-L6-v2` embeddings, Gemini 2.5 Flash
- Frontend: React 19, Vite, Tailwind 4

## Backend
```bash
cd backend
pip install -r requirements.txt
# create backend/.env containing: GOOGLE_API_KEY=your_key
python services/build_vector_db.py   # only needed to rebuild vector_db/
uvicorn app:app --reload
```

Endpoints: `POST /chat` (`{question}`), `POST /eligibility` (`{age, gender, occupation, income}`).
`/chat` is rate limited per IP (see `backend/config.py`).

## Frontend
```bash
cd frontend
npm install
# create frontend/.env containing: VITE_API_URL=http://localhost:8000
npm run dev
```
