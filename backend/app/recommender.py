from __future__ import annotations

import re
from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.sql.elements import ColumnElement
from sqlalchemy.orm import Session

from .embedding import cosine_similarity, embed_text
from .models import Course, Syllabus


DESCRIPTION_WEIGHT = 0.25
OUTCOME_WEIGHT = 0.45
TOPIC_WEIGHT = 0.30


def _collect_shared_terms(text_a: str, text_b: str, limit: int = 5) -> list[str]:
    tokens_a = set(re.findall(r"[a-zA-Z0-9]{3,}", (text_a or "").lower()))
    tokens_b = set(re.findall(r"[a-zA-Z0-9]{3,}", (text_b or "").lower()))
    overlap = sorted(tokens_a & tokens_b)
    return overlap[:limit]


@dataclass
class RecommendationScore:
    course: Course
    overall_score: float
    description_score: float
    learning_outcome_score: float
    weekly_topic_score: float
    explanation: str


def embed_syllabus_sections(syllabus: Syllabus) -> None:
    syllabus.description_embedding = embed_text(syllabus.description_text)
    syllabus.outcomes_embedding = embed_text(syllabus.outcomes_text)
    syllabus.weekly_topics_embedding = embed_text(syllabus.weekly_topics_text)


def _candidate_courses(
    session: Session,
    query_embedding: list[float] | None,
    limit: int = 80,
) -> list[Course]:
    stmt = select(Course).where(Course.is_active.is_(True))

    # If PostgreSQL+pgvector is available and embeddings exist, use ANN-friendly
    # distance ordering for candidate retrieval before weighted reranking.
    if query_embedding and not session.bind.dialect.name.startswith("sqlite"):
        vector_col: ColumnElement = Course.description_embedding
        stmt = stmt.where(vector_col.is_not(None)).order_by(
            vector_col.cosine_distance(query_embedding)
        )
    else:
        stmt = stmt.order_by(Course.updated_at.desc())

    stmt = stmt.limit(limit)
    return list(session.scalars(stmt).all())


def rank_courses_for_syllabus(
    session: Session,
    syllabus: Syllabus,
    top_n: int,
) -> list[RecommendationScore]:
    if syllabus.description_embedding is None:
        embed_syllabus_sections(syllabus)
        session.flush()

    courses = _candidate_courses(
        session,
        syllabus.description_embedding,
        limit=max(top_n * 12, 40),
    )
    ranked: list[RecommendationScore] = []

    for course in courses:
        if course.description_embedding is None:
            course.description_embedding = embed_text(course.description_text)
        if course.outcomes_embedding is None:
            course.outcomes_embedding = embed_text(course.outcomes_text)
        if course.weekly_topics_embedding is None:
            course.weekly_topics_embedding = embed_text(course.weekly_topics_text)

        description_score = cosine_similarity(
            syllabus.description_embedding,
            course.description_embedding,
        )
        learning_outcome_score = cosine_similarity(
            syllabus.outcomes_embedding,
            course.outcomes_embedding,
        )
        weekly_topic_score = cosine_similarity(
            syllabus.weekly_topics_embedding,
            course.weekly_topics_embedding,
        )
        overall_score = (
            (DESCRIPTION_WEIGHT * description_score)
            + (OUTCOME_WEIGHT * learning_outcome_score)
            + (TOPIC_WEIGHT * weekly_topic_score)
        )

        shared_terms = _collect_shared_terms(
            f"{syllabus.outcomes_text}\n{syllabus.weekly_topics_text}",
            f"{course.outcomes_text}\n{course.weekly_topics_text}",
            limit=5,
        )
        evidence = ", ".join(shared_terms) if shared_terms else "semantic thematic overlap"
        explanation = (
            "Ranked by weighted semantic similarity "
            f"(description {DESCRIPTION_WEIGHT:.2f}, outcomes {OUTCOME_WEIGHT:.2f}, "
            f"weekly topics {TOPIC_WEIGHT:.2f}). Evidence: {evidence}."
        )
        ranked.append(
            RecommendationScore(
                course=course,
                overall_score=overall_score,
                description_score=description_score,
                learning_outcome_score=learning_outcome_score,
                weekly_topic_score=weekly_topic_score,
                explanation=explanation,
            )
        )

    session.flush()
    ranked.sort(key=lambda item: item.overall_score, reverse=True)
    return ranked[:top_n]
