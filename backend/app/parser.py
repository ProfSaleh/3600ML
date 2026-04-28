from __future__ import annotations

import re
from dataclasses import dataclass
from io import BytesIO

from docx import Document
from pypdf import PdfReader


SECTION_HINTS = {
    "description": [
        "course description",
        "catalog description",
        "description",
        "about this course",
    ],
    "learning_outcomes": [
        "learning outcomes",
        "course learning outcomes",
        "course outcomes",
        "objectives",
        "learning objectives",
    ],
    "weekly_topics": [
        "weekly topics",
        "schedule",
        "course schedule",
        "weekly schedule",
        "topics by week",
        "course outline",
    ],
}


@dataclass
class ParsedSyllabus:
    description: str
    learning_outcomes: list[str]
    weekly_topics: list[str]


def extract_text_from_upload(filename: str, file_bytes: bytes) -> str:
    suffix = filename.rsplit(".", maxsplit=1)[-1].lower() if "." in filename else ""
    if suffix == "pdf":
        return _extract_pdf_text(file_bytes)
    if suffix == "docx":
        return _extract_docx_text(file_bytes)
    return file_bytes.decode("utf-8", errors="ignore")


def _extract_pdf_text(file_bytes: bytes) -> str:
    reader = PdfReader(BytesIO(file_bytes))
    pages = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(pages).strip()


def _extract_docx_text(file_bytes: bytes) -> str:
    doc = Document(BytesIO(file_bytes))
    return "\n".join([para.text for para in doc.paragraphs if para.text.strip()]).strip()


def split_syllabus_sections(text: str) -> ParsedSyllabus:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    lowered = [line.lower() for line in lines]

    indexes: dict[str, int | None] = {
        "description": None,
        "learning_outcomes": None,
        "weekly_topics": None,
    }
    for i, line in enumerate(lowered):
        for key, hints in SECTION_HINTS.items():
            if indexes[key] is None and any(hint in line for hint in hints):
                indexes[key] = i

    if indexes["description"] is None:
        indexes["description"] = 0 if lines else None
    if indexes["learning_outcomes"] is None:
        indexes["learning_outcomes"] = _find_first_bullet_index(lines)
    if indexes["weekly_topics"] is None:
        indexes["weekly_topics"] = _find_weekly_start_index(lines)

    segments = _slice_segments(lines, indexes)

    description_text = segments["description"] or "\n".join(lines[: min(len(lines), 8)])
    outcomes = _parse_bullets_or_lines(segments["learning_outcomes"], min_length=12, limit=12)
    topics = _parse_topics(segments["weekly_topics"])

    if not outcomes:
        outcomes = _guess_outcomes(lines)
    if not topics:
        topics = _guess_topics(lines)

    return ParsedSyllabus(
        description=description_text.strip(),
        learning_outcomes=outcomes[:12],
        weekly_topics=topics[:16],
    )


def _slice_segments(lines: list[str], indexes: dict[str, int | None]) -> dict[str, str]:
    segments = {"description": "", "learning_outcomes": "", "weekly_topics": ""}
    boundaries = sorted(
        [(key, idx) for key, idx in indexes.items() if idx is not None],
        key=lambda pair: pair[1],
    )
    for i, (section_name, start_idx) in enumerate(boundaries):
        end_idx = boundaries[i + 1][1] if i + 1 < len(boundaries) else len(lines)
        chunk = lines[start_idx:end_idx]
        segments[section_name] = "\n".join(chunk).strip()
    return segments


def _parse_bullets_or_lines(section_text: str, min_length: int, limit: int) -> list[str]:
    if not section_text:
        return []
    items: list[str] = []
    for line in section_text.splitlines():
        cleaned = re.sub(r"^[\-\*\d\.\)\(]+\s*", "", line).strip(" -:\t")
        if len(cleaned) >= min_length:
            items.append(cleaned)
    deduped = list(dict.fromkeys(items))
    return deduped[:limit]


def _parse_topics(section_text: str) -> list[str]:
    if not section_text:
        return []
    topics: list[str] = []
    for line in section_text.splitlines():
        clean_line = line.strip()
        if not clean_line:
            continue
        if re.search(r"\b(week|module)\b", clean_line.lower()):
            topics.append(clean_line)
        elif clean_line.startswith(("-", "*")):
            topics.append(clean_line[1:].strip())
    if not topics:
        topics = _parse_bullets_or_lines(section_text, min_length=8, limit=16)
    return list(dict.fromkeys(topics))[:16]


def _guess_outcomes(lines: list[str]) -> list[str]:
    candidates = []
    for line in lines:
        lower = line.lower()
        if any(verb in lower for verb in ("analyze", "apply", "design", "evaluate", "build", "explain")):
            if len(line) >= 12:
                candidates.append(line.strip())
    return list(dict.fromkeys(candidates))[:10]


def _guess_topics(lines: list[str]) -> list[str]:
    candidates = []
    for line in lines:
        lower = line.lower()
        if re.search(r"\bweek\s*\d+\b", lower) or re.search(r"\bmodule\s*\d+\b", lower):
            candidates.append(line.strip())
    return list(dict.fromkeys(candidates))[:16]


def _find_first_bullet_index(lines: list[str]) -> int | None:
    for i, line in enumerate(lines):
        if re.match(r"^(\-|\*|\d+[\.\)])\s+", line):
            return i
    return None


def _find_weekly_start_index(lines: list[str]) -> int | None:
    for i, line in enumerate(lines):
        if re.search(r"\bweek\s*\d+\b", line.lower()):
            return i
    return None
