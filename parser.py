"""Utilities for parsing syllabus files and extracting sections."""

from __future__ import annotations

import re
from collections import OrderedDict
from io import BytesIO
from typing import Dict, List

from docx import Document
from pypdf import PdfReader


SECTION_ALIASES = {
    "Course Description": [
        "course description",
        "description",
        "catalog description",
        "about this course",
        "course overview",
        "overview",
    ],
    "Learning Outcomes": [
        "learning outcomes",
        "course outcomes",
        "student learning outcomes",
        "objectives",
        "course objectives",
    ],
    "Assignments": [
        "assignments",
        "projects",
        "coursework",
        "major assignments",
        "deliverables",
    ],
    "Weekly Schedule": [
        "weekly schedule",
        "course schedule",
        "calendar",
        "timeline",
        "topics by week",
    ],
    "Assessment": [
        "assessment",
        "grading",
        "evaluation",
        "grading policy",
        "rubric",
    ],
    "Policies": [
        "course policies",
        "policies",
        "attendance",
        "academic integrity",
    ],
}


def _normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


SectionMap = Dict[str, str]


def extract_text_from_upload(filename: str, payload: bytes) -> str:
    """Extract text from uploaded syllabus content."""
    filename = filename.lower()

    if filename.endswith(".pdf"):
        return _extract_pdf_text(payload)
    if filename.endswith(".docx"):
        return _extract_docx_text(payload)
    if filename.endswith(".txt"):
        return _decode_text(payload)

    raise ValueError("Unsupported file type. Please upload PDF, DOCX, or TXT.")


def _extract_pdf_text(payload: bytes) -> str:
    reader = PdfReader(BytesIO(payload))
    chunks = [page.extract_text() or "" for page in reader.pages]
    return _normalize_text("\n".join(chunks))


def _extract_docx_text(payload: bytes) -> str:
    document = Document(BytesIO(payload))
    chunks = [paragraph.text for paragraph in document.paragraphs]
    return _normalize_text("\n".join(chunks))


def _decode_text(payload: bytes) -> str:
    try:
        text = payload.decode("utf-8")
    except UnicodeDecodeError:
        text = payload.decode("latin-1")
    return _normalize_text(text)


def split_into_sections(text: str) -> SectionMap:
    """Extract common syllabus sections using heading detection."""
    text = _normalize_text(text)
    sections: "OrderedDict[str, List[str]]" = OrderedDict(
        (
            ("Course Description", []),
            ("Learning Outcomes", []),
            ("Assignments", []),
            ("Weekly Schedule", []),
            ("Assessment", []),
            ("Policies", []),
            ("General", []),
        )
    )

    current_section = "General"
    for raw_line in text.split("\n"):
        line = raw_line.strip()
        if not line:
            sections[current_section].append("")
            continue

        candidate = _section_from_heading(line)
        if candidate:
            current_section = candidate
            continue

        sections[current_section].append(line)

    return {name: _normalize_text("\n".join(lines)) for name, lines in sections.items()}


def _section_from_heading(line: str) -> str | None:
    cleaned = line.strip().lower().rstrip(":")
    if len(cleaned) > 80:
        return None

    for section, aliases in SECTION_ALIASES.items():
        for alias in aliases:
            if cleaned == alias or cleaned.startswith(f"{alias} "):
                return section
    return None


def sentence_list(text: str) -> List[str]:
    """Return non-empty sentence candidates for evidence extraction."""
    pieces = re.split(r"(?<=[.!?])\s+|\n+", text)
    return [piece.strip() for piece in pieces if piece.strip()]


def parse_line_items(text: str) -> List[dict]:
    """
    Parse text line-by-line and attach inferred section context.
    Returns non-empty content lines with source line numbers.
    """
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    current_section = "General"
    item_number = 0
    section_counters: Dict[str, int] = {}
    items: List[dict] = []

    for line_number, raw_line in enumerate(normalized.split("\n"), start=1):
        line = raw_line.strip()
        if not line:
            continue

        candidate = _section_from_heading(line)
        if candidate:
            current_section = candidate
            continue

        item_number += 1
        section_counters[current_section] = section_counters.get(current_section, 0) + 1
        items.append(
            {
                "line_number": line_number,
                "item_number": item_number,
                "section_item_number": section_counters[current_section],
                "section": current_section,
                "text": line,
            }
        )

    return items


def extract_weekly_breakdown(sections: SectionMap) -> List[dict]:
    """
    Extract assignment/activity lines with week/module context.
    Prioritizes Weekly Schedule, Assignments, and Assessment sections.
    """
    weekly_sources = ["Weekly Schedule", "Assignments", "Assessment", "General"]
    activity_keywords = [
        "assignment",
        "discussion",
        "dq",
        "quiz",
        "exam",
        "project",
        "presentation",
        "lab",
        "reflection",
        "paper",
        "report",
    ]
    week_pattern = re.compile(r"\b(week|module|unit)\s*\d+\b", re.IGNORECASE)
    seen = set()
    items: List[dict] = []

    for section_name in weekly_sources:
        content = sections.get(section_name, "")
        if not content:
            continue
        for raw_line in content.split("\n"):
            line = raw_line.strip(" -\t")
            if len(line) < 10:
                continue
            line_lc = line.lower()
            has_activity = any(word in line_lc for word in activity_keywords)
            has_week = bool(week_pattern.search(line))
            if not (has_activity or has_week):
                continue
            norm = line_lc
            if norm in seen:
                continue
            seen.add(norm)

            week_match = week_pattern.search(line)
            week_label = week_match.group(0).title() if week_match else section_name

            activity_type = "activity"
            for keyword in activity_keywords:
                if keyword in line_lc:
                    activity_type = keyword
                    break

            items.append(
                {
                    "section": section_name,
                    "week_label": week_label,
                    "activity_type": activity_type,
                    "line": line,
                }
            )

    return items[:60]
