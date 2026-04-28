from __future__ import annotations

from collections.abc import Generator

from pgvector.sqlalchemy import Vector
from sqlalchemy import JSON, create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from .config import settings


def _create_engine() -> Engine:
    # SQLite is kept as a fallback for quick local bootstrapping.
    if settings.database_url.startswith("sqlite"):
        return create_engine(
            settings.database_url,
            connect_args={"check_same_thread": False},
            future=True,
        )
    return create_engine(settings.database_url, future=True)


engine = _create_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=Session)
Base = declarative_base()

def embedding_column_type(dimensions: int):
    if engine.dialect.name == "postgresql":
        return Vector(dimensions)
    return JSON


def ensure_vector_extension() -> None:
    if engine.dialect.name != "postgresql":
        return

    with engine.begin() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
 

def create_vector_indexes() -> None:
    if engine.dialect.name != "postgresql":
        return

    with engine.begin() as conn:
        conn.execute(
            text(
                "CREATE INDEX IF NOT EXISTS idx_courses_description_embedding_hnsw "
                "ON courses USING hnsw (description_embedding vector_cosine_ops)"
            )
        )
        conn.execute(
            text(
                "CREATE INDEX IF NOT EXISTS idx_courses_outcomes_embedding_hnsw "
                "ON courses USING hnsw (outcomes_embedding vector_cosine_ops)"
            )
        )
        conn.execute(
            text(
                "CREATE INDEX IF NOT EXISTS idx_courses_weekly_embedding_hnsw "
                "ON courses USING hnsw (weekly_topics_embedding vector_cosine_ops)"
            )
        )


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
