from __future__ import annotations

from pathlib import Path

from fastapi import Depends, FastAPI, File, Form, HTTPException, Query, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy import inspect, select
from sqlalchemy.orm import Session

from .auth import create_access_token, get_current_user, hash_password, verify_password
from .bootstrap import ensure_bootstrap_admin
from .catalog_ingest import ingest_from_coursera_api, ingest_from_json_feed
from .config import settings
from .database import Base, create_vector_indexes, ensure_vector_extension, engine, get_db
from .models import Course, RecommendationResult, RecommendationRun, Syllabus, User
from .parser import extract_text_from_upload, split_syllabus_sections
from .recommender import (
    DESCRIPTION_WEIGHT,
    OUTCOME_WEIGHT,
    TOPIC_WEIGHT,
    embed_syllabus_sections,
    rank_courses_for_syllabus,
)
from .seed import seed_courses_if_empty
from .schemas import (
    AuthResponse,
    CatalogIngestRequest,
    CatalogIngestResponse,
    CourseRecommendation,
    CourseSummary,
    RecommendationResponse,
    SectionedSyllabus,
    UploadSyllabusResponse,
    UserCreateRequest,
    UserLoginRequest,
    UserResponse,
)


def _parse_cors_origins() -> list[str]:
    raw = (settings.cors_origins or "").strip()
    if not raw:
        return ["*"]
    if raw == "*":
        return ["*"]
    return [origin.strip() for origin in raw.split(",") if origin.strip()]


app = FastAPI(
    title=settings.app_name,
    description="Upload a syllabus and get top active Coursera course recommendations.",
    version="0.2.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=_parse_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def initialize_database() -> None:
    ensure_vector_extension()
    if _sqlite_schema_outdated():
        Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    create_vector_indexes()
    with Session(engine) as session:
        ensure_bootstrap_admin(session)
        seed_courses_if_empty(session)


def _sqlite_schema_outdated() -> bool:
    if engine.dialect.name != "sqlite":
        return False

    inspector = inspect(engine)
    if "courses" not in inspector.get_table_names():
        return False

    required_columns = {
        "provider",
        "provider_course_id",
        "language_code",
        "description_embedding",
        "outcomes_embedding",
        "weekly_topics_embedding",
    }
    existing_columns = {column["name"] for column in inspector.get_columns("courses")}
    return not required_columns.issubset(existing_columns)


@app.on_event("startup")
def on_startup() -> None:
    initialize_database()


FRONTEND_INDEX = Path(__file__).resolve().parents[2] / "frontend" / "index.html"
UPLOADS_DIR = Path(__file__).resolve().parents[1] / "uploads"
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)


@app.get("/health")
def healthcheck() -> dict:
    return {"status": "ok", "environment": settings.app_env}


@app.get("/")
def frontend() -> FileResponse:
    if not FRONTEND_INDEX.exists():
        raise HTTPException(status_code=404, detail="Frontend not found.")
    return FileResponse(FRONTEND_INDEX)


@app.post("/api/auth/register", response_model=AuthResponse)
def register_user(
    payload: UserCreateRequest,
    make_admin: bool = Query(default=False),
    db: Session = Depends(get_db),
) -> AuthResponse:
    email = payload.email.lower()
    existing = db.scalar(select(User).where(User.email == email))
    if existing:
        raise HTTPException(status_code=409, detail="A user with this email already exists.")

    has_admin = db.scalar(select(User).where(User.is_admin.is_(True)))
    user = User(
        email=email,
        full_name=payload.full_name.strip(),
        department=payload.department.strip(),
        password_hash=hash_password(payload.password),
        is_admin=bool(make_admin and not has_admin),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token(subject=user.email)
    return AuthResponse(access_token=token, user=UserResponse.model_validate(user))


@app.post("/api/auth/login", response_model=AuthResponse)
def login_user(payload: UserLoginRequest, db: Session = Depends(get_db)) -> AuthResponse:
    user = db.scalar(select(User).where(User.email == payload.email.lower()))
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    token = create_access_token(subject=user.email)
    return AuthResponse(access_token=token, user=UserResponse.model_validate(user))


@app.get("/api/auth/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)) -> UserResponse:
    return UserResponse.model_validate(current_user)


@app.get("/api/auth/bootstrap-status")
def bootstrap_status() -> dict[str, bool]:
    return {
        "bootstrap_admin_configured": bool(
            settings.bootstrap_admin_email and settings.bootstrap_admin_password
        )
    }


@app.post("/api/catalog/ingest", response_model=CatalogIngestResponse)
def ingest_catalog(
    payload: CatalogIngestRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> CatalogIngestResponse:
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only admin users can run ingestion.")

    if payload.source == "coursera_api":
        run = ingest_from_coursera_api(db, triggered_by=current_user)
    else:
        run = ingest_from_json_feed(
            db,
            triggered_by=current_user,
            feed_path=payload.feed_path,
        )

    return CatalogIngestResponse(
        ingestion_run_id=run.id,
        source=run.source,
        status=run.status,
        ingested_count=run.ingested_count,
        created_count=run.created_count,
        updated_count=run.updated_count,
        error_message=run.error_message or "",
    )


@app.get("/api/catalog/ingest/{ingestion_run_id}", response_model=CatalogIngestResponse)
def get_ingestion_run(
    ingestion_run_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> CatalogIngestResponse:
    run = db.scalar(select(CatalogIngestionRun).where(CatalogIngestionRun.id == ingestion_run_id))
    if not run:
        raise HTTPException(status_code=404, detail="Ingestion run not found.")
    if not current_user.is_admin and run.triggered_by_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this ingestion run.")

    return CatalogIngestResponse(
        ingestion_run_id=run.id,
        source=run.source,
        status=run.status,
        ingested_count=run.ingested_count,
        created_count=run.created_count,
        updated_count=run.updated_count,
        error_message=run.error_message or "",
    )


@app.get("/api/courses", response_model=list[CourseSummary])
def list_courses(
    active_only: bool = True,
    limit: int = Query(default=50, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[CourseSummary]:
    stmt = select(Course)
    if active_only:
        stmt = stmt.where(Course.is_active.is_(True))
    stmt = stmt.order_by(Course.updated_at.desc()).limit(limit)
    rows = list(db.scalars(stmt).all())
    return [
        CourseSummary(
            id=course.id,
            provider_course_id=course.provider_course_id,
            title=course.title,
            partner_name=course.partner_name,
            level=course.level,
            language_code=course.language_code,
            url=course.url,
            is_active=course.is_active,
        )
        for course in rows
    ]


@app.post("/api/syllabi/upload", response_model=UploadSyllabusResponse)
async def upload_syllabus(
    title: str = Form(..., min_length=2, max_length=255),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> UploadSyllabusResponse:
    content = await file.read()
    text = extract_text_from_upload(file.filename, content)
    parsed = split_syllabus_sections(text)

    safe_name = file.filename.replace("/", "_")
    file_path = UPLOADS_DIR / f"{current_user.id}_{safe_name}"
    file_path.write_bytes(content)

    syllabus = Syllabus(
        uploaded_by_id=current_user.id,
        title=title.strip(),
        filename=file.filename,
        stored_path=str(file_path),
        raw_text=text,
        description_text=parsed.description,
        outcomes_text="\n".join(parsed.learning_outcomes),
        weekly_topics_text="\n".join(parsed.weekly_topics),
    )
    embed_syllabus_sections(syllabus)
    db.add(syllabus)
    db.commit()
    db.refresh(syllabus)

    return UploadSyllabusResponse(
        syllabus_id=syllabus.id,
        parsed=SectionedSyllabus(
            description=parsed.description,
            learning_outcomes=parsed.learning_outcomes,
            weekly_topics=parsed.weekly_topics,
        ),
    )


@app.post("/api/recommendations/{syllabus_id}", response_model=RecommendationResponse)
def generate_recommendations(
    syllabus_id: int,
    top_n: int = Query(default=5, ge=1, le=20),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> RecommendationResponse:
    syllabus = db.scalar(
        select(Syllabus).where(
            Syllabus.id == syllabus_id,
            Syllabus.uploaded_by_id == current_user.id,
        )
    )
    if not syllabus:
        raise HTTPException(status_code=404, detail="Syllabus not found.")

    ranked = rank_courses_for_syllabus(session=db, syllabus=syllabus, top_n=top_n)
    run = RecommendationRun(
        syllabus_id=syllabus.id,
        requested_by_id=current_user.id,
        top_n=top_n,
        weight_description=DESCRIPTION_WEIGHT,
        weight_learning_outcome=OUTCOME_WEIGHT,
        weight_weekly_topic=TOPIC_WEIGHT,
        status="completed",
    )
    db.add(run)
    db.flush()

    response_items: list[CourseRecommendation] = []
    for rank_position, rec in enumerate(ranked, start=1):
        db.add(
            RecommendationResult(
                run_id=run.id,
                course_id=rec.course.id,
                rank=rank_position,
                overall_score=rec.overall_score,
                description_score=rec.description_score,
                learning_outcome_score=rec.learning_outcome_score,
                weekly_topic_score=rec.weekly_topic_score,
                explanation=rec.explanation,
            )
        )
        response_items.append(
            CourseRecommendation(
                rank=rank_position,
                course_id=rec.course.id,
                title=rec.course.title,
                provider=rec.course.provider,
                partner_name=rec.course.partner_name,
                level=rec.course.level,
                url=rec.course.url,
                overall_score=rec.overall_score,
                description_score=rec.description_score,
                learning_outcome_score=rec.learning_outcome_score,
                weekly_topic_score=rec.weekly_topic_score,
                explanation=rec.explanation,
            )
        )

    db.commit()
    return RecommendationResponse(
        run_id=run.id,
        syllabus_id=syllabus.id,
        top_n=top_n,
        weights={
            "description": DESCRIPTION_WEIGHT,
            "learning_outcome": OUTCOME_WEIGHT,
            "weekly_topic": TOPIC_WEIGHT,
        },
        recommendations=response_items,
    )
