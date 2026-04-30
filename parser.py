"""Utilities for parsing syllabus files and extracting sections."""

from __future__ import annotations

import re
from collections import OrderedDict
from io import BytesIO
from typing import Dict, List

from docx import Document
from pypdf import PdfReader


SECTION_ALIASES = {
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
