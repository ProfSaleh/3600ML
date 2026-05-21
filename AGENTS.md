# AGENTS.md

## Cursor Cloud specific instructions

### Repository structure

This is a branch-based monorepo. The `main` branch contains only a README. Each product lives on its own feature branch:

| Branch | Product | Stack |
|--------|---------|-------|
| `cursor/coursera-syllabus-app-b839` | Syllabus-to-Coursera Recommender | FastAPI + vanilla JS |
| `cursor/nace-syllabus-mvp-3dc8` | NACE Competency Assignment Assistant | Streamlit |
| `cursor/threejs-car-dodge-7e5a` | Three.js Car Dodger Game | Static HTML/JS/CSS |

To work on a product, use `git worktree add /tmp/<name> origin/<branch>` rather than switching the main checkout.

### Running the products

**Coursera Recommender** (branch `cursor/coursera-syllabus-app-b839`):
```bash
cd backend && cp .env.example .env   # first time only
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
- Uses SQLite by default (`sqlite:///./app.db`), no external DB required.
- Uses `local-hash` embedding provider by default (no OpenAI key needed).
- Frontend served at `GET /`, API docs at `/docs`.

**NACE Assistant** (branch `cursor/nace-syllabus-mvp-3dc8`):
```bash
streamlit run app.py --server.port 8501 --server.headless true
```

**Three.js Game** (branch `cursor/threejs-car-dodge-7e5a`):
```bash
python3 -m http.server 8080
```

### Testing

- **NACE Assistant** has a pytest suite: `cd /tmp/nace-app && pytest -q tests/`
- **Coursera Recommender** has no automated tests but can be tested via API:
  - `GET /health` returns `{"status":"ok"}`
  - Register → Login → Upload syllabus → Get recommendations (see README on that branch)
- **Three.js Game** has no automated tests; open in browser to verify.

### Gotchas

- The Coursera app's `pydantic-settings` reads `.env` from the CWD, so you must run `uvicorn` from inside the `backend/` directory.
- The `pgvector` and `psycopg[binary]` pip packages install without error even without PostgreSQL; they are only used when `DATABASE_URL` points to a Postgres instance.
- Python 3.12+ is required for both Python apps.
