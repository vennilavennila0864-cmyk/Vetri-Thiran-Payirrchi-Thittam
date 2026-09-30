# LegalEase — AI-Powered Legal Document Generator

A full-stack starter project for generating customizable legal documents with AI.

## Stack
- Frontend: React + TypeScript + Vite
- Backend: FastAPI + SQLAlchemy
- Database: SQLite by default (easy to switch to PostgreSQL)
- Document export: DOCX, PDF, TXT
- AI: provider-agnostic service interface

## Quick start

### Backend
```bash
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
# source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API docs: http://localhost:8000/docs

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Frontend: http://localhost:5173

## AI configuration
Set `AI_API_KEY` in `backend/.env` when connecting an AI provider. The included service has a deterministic demo mode so the project works without an API key.

## Legal notice
This software is an AI-assisted document drafting tool. Generated documents are not a substitute for advice from a qualified lawyer and should be reviewed for the relevant jurisdiction and circumstances.
