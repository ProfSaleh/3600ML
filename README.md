# Syllabus-to-Coursera Recommender (MVP)

Web app for faculty to upload a course syllabus and receive the top 5 active Coursera course recommendations based on:

1. Course description
2. Course learning outcomes
3. Weekly topics

The matching score uses weighted section alignment:

- Description: 0.25
- Learning outcomes: 0.45
- Weekly topics: 0.30

## Stack

- **Backend:** FastAPI + SQLAlchemy + SQLite
- **Frontend:** Vanilla HTML/CSS/JS
- **Parsing:** `pypdf` for PDF, `python-docx` for DOCX

## Run locally

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then open:

- http://127.0.0.1:8000

## API endpoints

- `GET /health`
- `POST /api/syllabi/upload` (multipart form with `faculty_name`, `department`, `title`, `file`)
- `POST /api/recommendations/{syllabus_id}?top_n=5`

## Notes

- On startup, the app seeds a small sample active Coursera course catalog.
- Upload files are stored under `backend/uploads`.
- Database file is `backend/app.db`.
