# Syllabus-to-Coursera Recommender (Upgraded)

Full-stack web app for faculty to upload syllabi and receive top semantic course recommendations from active Coursera catalog content.

This version includes:

- Faculty authentication (JWT)
- Admin-only catalog ingestion (JSON feed and Coursera API adapter)
- Semantic embeddings for syllabus/course sections
- PostgreSQL + pgvector support (with SQLite fallback)
- Weighted recommendation scoring:
  - Description: 0.25
  - Learning outcomes: 0.45
  - Weekly topics: 0.30

## Architecture

- **Backend:** FastAPI + SQLAlchemy
- **Auth:** JWT (`python-jose`) + password hashing (`passlib`)
- **Embeddings:** OpenAI or deterministic local fallback
- **Vector DB:** pgvector (recommended), JSON fallback for SQLite
- **Frontend:** Vanilla HTML/CSS/JS
- **Parsing:** `pypdf` (PDF), `python-docx` (DOCX)

## Quickstart

1. Install backend dependencies:

```bash
cd backend
pip3 install --user -r requirements.txt
```

2. Create env file:

```bash
cp .env.example .env
```

3. Run API:

```bash
uvicorn app.main:app --reload
```

4. Open:

- http://127.0.0.1:8000

## Environment variables

Use `backend/.env.example` as reference. Key values:

- `DATABASE_URL`  
  - Recommended: `postgresql+psycopg://...` (with pgvector extension)
  - Local fallback: `sqlite:///./app.db`
- `EMBEDDING_PROVIDER` = `local-hash` or `openai`
- `OPENAI_API_KEY` required when `EMBEDDING_PROVIDER=openai`
- `COURSERA_API_TOKEN` required for `coursera_api` ingestion source
- Optional bootstrap admin:
  - `BOOTSTRAP_ADMIN_EMAIL`
  - `BOOTSTRAP_ADMIN_PASSWORD`

## Catalog ingestion

### 1) JSON feed ingestion

Sample feed included:

- `backend/data/coursera_sample_feed.json`

Admin can trigger ingestion from UI or API:

- `POST /api/catalog/ingest` with body:

```json
{
  "source": "json_feed",
  "feed_path": "data/coursera_sample_feed.json"
}
```

### 2) Coursera API ingestion

Endpoint adapter:

- `GET {COURSERA_API_BASE_URL}/onDemandCourses.v1`

Admin trigger:

```json
{
  "source": "coursera_api"
}
```

> Note: exact fields available depend on the Coursera API credentials and response shape.

## API summary

- `GET /health`
- `GET /api/auth/bootstrap-status`
- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/auth/me` (Bearer token)
- `POST /api/catalog/ingest` (admin only, Bearer token)
- `GET /api/courses` (Bearer token)
- `POST /api/syllabi/upload` (Bearer token, multipart with `title`, `file`)
- `POST /api/recommendations/{syllabus_id}?top_n=5` (Bearer token)

## Data model highlights

- `users`
- `syllabi` (with section text + embeddings)
- `courses` (catalog content + embeddings)
- `catalog_ingestion_runs`
- `recommendation_runs`
- `recommendation_results`

## Notes

- Uploads are stored at `backend/uploads/`.
- SQLite works for local testing, but pgvector + PostgreSQL is strongly recommended for production retrieval quality and performance.
