from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import httpx
from sqlalchemy.orm import Session

from .config import settings
from .embedding import embed_text
from .models import CatalogIngestionRun, Course, User


@dataclass
class IngestionSummary:
    source: str
    ingested_count: int
    created_count: int
    updated_count: int


def _normalize_course_payload(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "provider": item.get("provider", "coursera"),
        "provider_course_id": str(
            item.get("provider_course_id")
            or item.get("id")
            or item.get("slug")
            or item.get("course_id")
        ),
        "title": item.get("title", "").strip(),
        "partner_name": item.get("partner_name", "").strip(),
        "level": item.get("level", "Mixed").strip() or "Mixed",
        "language_code": item.get("language_code", "en").strip() or "en",
        "url": item.get("url", "").strip(),
        "is_active": bool(item.get("is_active", True)),
        "description_text": item.get("description_text", "").strip(),
        "outcomes_text": item.get("outcomes_text", "").strip(),
        "weekly_topics_text": item.get("weekly_topics_text", "").strip(),
    }


def _upsert_courses(
    session: Session,
    records: list[dict[str, Any]],
    source: str,
) -> IngestionSummary:
    created_count = 0
    updated_count = 0

    for raw in records:
        payload = _normalize_course_payload(raw)
        if not payload["provider_course_id"] or not payload["title"] or not payload["url"]:
            continue

        existing = (
            session.query(Course)
            .filter(
                Course.provider == payload["provider"],
                Course.provider_course_id == payload["provider_course_id"],
            )
            .first()
        )

        if existing:
            existing.title = payload["title"]
            existing.partner_name = payload["partner_name"]
            existing.level = payload["level"]
            existing.language_code = payload["language_code"]
            existing.url = payload["url"]
            existing.is_active = payload["is_active"]
            existing.description_text = payload["description_text"]
            existing.outcomes_text = payload["outcomes_text"]
            existing.weekly_topics_text = payload["weekly_topics_text"]
            updated_count += 1
            course = existing
        else:
            course = Course(**payload)
            session.add(course)
            created_count += 1

        full_text = " ".join(
            [
                course.description_text or "",
                course.outcomes_text or "",
                course.weekly_topics_text or "",
            ]
        ).strip()
        if full_text:
            course.description_embedding = embed_text(course.description_text)
            course.outcomes_embedding = embed_text(course.outcomes_text)
            course.weekly_topics_embedding = embed_text(course.weekly_topics_text)

    session.flush()
    return IngestionSummary(
        source=source,
        ingested_count=created_count + updated_count,
        created_count=created_count,
        updated_count=updated_count,
    )


def _extract_items(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if isinstance(payload, dict):
        for key in ("courses", "elements", "results"):
            value = payload.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]
    return []


def ingest_from_json_feed(
    session: Session,
    triggered_by: User,
    feed_path: str | None = None,
) -> CatalogIngestionRun:
    path = Path(feed_path or settings.coursera_default_feed_path)
    run = CatalogIngestionRun(
        provider="coursera",
        source="json_feed",
        status="running",
        triggered_by_id=triggered_by.id,
    )
    session.add(run)
    session.flush()

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        items = _extract_items(payload)
        summary = _upsert_courses(session, items, source="json_feed")
        run.status = "completed"
        run.ingested_count = summary.ingested_count
        run.created_count = summary.created_count
        run.updated_count = summary.updated_count
    except Exception as exc:  # noqa: BLE001
        run.status = "failed"
        run.error_message = str(exc)
    session.commit()
    return run


def ingest_from_coursera_api(session: Session, triggered_by: User) -> CatalogIngestionRun:
    run = CatalogIngestionRun(
        provider="coursera",
        source="coursera_api",
        status="running",
        triggered_by_id=triggered_by.id,
    )
    session.add(run)
    session.flush()

    if not settings.coursera_api_token:
        run.status = "failed"
        run.error_message = "COURSERA_API_TOKEN is not configured."
        session.commit()
        return run

    url = f"{settings.coursera_api_base_url.rstrip('/')}/onDemandCourses.v1"
    headers = {"Authorization": f"Bearer {settings.coursera_api_token}"}
    params = {"q": "search", "limit": settings.coursera_api_page_size}

    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.get(url, headers=headers, params=params)
            response.raise_for_status()
            payload = response.json()
        items = _extract_items(payload)
        summary = _upsert_courses(session, items, source="coursera_api")
        run.status = "completed"
        run.ingested_count = summary.ingested_count
        run.created_count = summary.created_count
        run.updated_count = summary.updated_count
    except Exception as exc:  # noqa: BLE001
        run.status = "failed"
        run.error_message = str(exc)

    session.commit()
    return run
