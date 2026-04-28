from __future__ import annotations

from pathlib import Path
from typing import List

from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import Course, RecommendationResult, RecommendationRun, Syllabus
from .parser import extract_text_from_upload, split_syllabus_sections
from .recommender import rank_courses_for_sections
from .schemas import CourseRecommendation, RecommendationResponse, SectionedSyllabus, UploadSyllabusResponse
from .seed import seed_courses_if_empty


app = FastAPI(
    title="Syllabus to Coursera Recommender",
    description="Upload a syllabus and get top 5 active Coursera course recommendations.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def initialize_database() -> None:
    Base.metadata.create_all(bind=engine)
    with Session(engine) as session:
        seed_courses_if_empty(session)


@app.on_event("startup")
def on_startup() -> None:
    initialize_database()


FRONTEND_INDEX = Path(__file__).resolve().parents[2] / "frontend" / "index.html"


@app.get("/health")
def healthcheck() -> dict:
    return {"status": "ok"}


@app.get("/")
def frontend() -> FileResponse:
    if not FRONTEND_INDEX.exists():
        raise HTTPException(status_code=404, detail="Frontend not found.")
    return FileResponse(FRONTEND_INDEX)


@app.post("/api/syllabi/upload", response_model=UploadSyllabusResponse)
async def upload_syllabus(
    faculty_name: str = Form(...),
    department: str = Form(...),
    title: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> UploadSyllabusResponse:
    content = await file.read()
    text = extract_text_from_upload(file.filename, content)
    parsed = split_syllabus_sections(text)

    uploads_dir = Path(__file__).resolve().parents[1] / "uploads"
    uploads_dir.mkdir(parents=True, exist_ok=True)
    safe_name = file.filename.replace("/", "_")
    file_path = uploads_dir / safe_name
    file_path.write_bytes(content)

    syllabus = Syllabus(
        faculty_name=faculty_name,
        department=department,
        title=title,
        filename=file.filename,
        stored_path=str(file_path),
        raw_text=text,
        description_text=parsed.description,
        outcomes_text="\n".join(parsed.learning_outcomes),
        weekly_topics_text="\n".join(parsed.weekly_topics),
    )
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
    top_n: int = 5,
    db: Session = Depends(get_db),
) -> RecommendationResponse:
    syllabus = db.query(Syllabus).filter(Syllabus.id == syllabus_id).first()
    if not syllabus:
        raise HTTPException(status_code=404, detail="Syllabus not found.")

    if top_n < 1 or top_n > 20:
        raise HTTPException(status_code=400, detail="top_n must be between 1 and 20.")

    courses: List[Course] = (
        db.query(Course).filter(Course.is_active.is_(True)).order_by(Course.title).all()
    )
    ranked = rank_courses_for_sections(
        description=syllabus.description_text,
        outcomes_text=syllabus.outcomes_text,
        weekly_topics_text=syllabus.weekly_topics_text,
        courses=courses,
        top_n=top_n,
    )

    run = RecommendationRun(
        syllabus_id=syllabus.id,
        top_n=top_n,
        weight_description=0.25,
        weight_learning_outcome=0.45,
        weight_weekly_topic=0.30,
        status="completed",
    )
    db.add(run)
    db.flush()

    response_items: list[CourseRecommendation] = []
    for rank_position, rec in enumerate(ranked, start=1):
        result = RecommendationResult(
            run_id=run.id,
            course_id=rec.course.id,
            rank=rank_position,
            overall_score=rec.overall_score,
            description_score=rec.description_score,
            learning_outcome_score=rec.learning_outcome_score,
            weekly_topic_score=rec.weekly_topic_score,
            explanation=rec.explanation,
        )
        db.add(result)

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
            "description": run.weight_description,
            "learning_outcome": run.weight_learning_outcome,
            "weekly_topic": run.weight_weekly_topic,
        },
        recommendations=response_items,
    )
