import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from nace_engine import evaluate_syllabus, generate_recommendations, render_revised_syllabus
from parser import split_into_sections


SAMPLE_SYLLABUS = """
Course Objectives:
Students will analyze case studies and present findings to varied audiences.

Assignments:
Group project with peer review and final written report.

Weekly Schedule:
Week 4: Team facilitation and reflection checkpoint.

Grading Policy:
Presentations are graded with a communication rubric and quality standards.
"""


def test_split_into_sections_detects_common_headings():
    sections = split_into_sections(SAMPLE_SYLLABUS)

    assert "Learning Outcomes" in sections
    assert "Assignments" in sections
    assert "Weekly Schedule" in sections
    assert "Assessment" in sections

    assert "analyze case studies" in sections["Learning Outcomes"].lower()
    assert "peer review" in sections["Assignments"].lower()


def test_evaluate_syllabus_returns_all_competencies():
    sections = split_into_sections(SAMPLE_SYLLABUS)
    analysis = evaluate_syllabus(SAMPLE_SYLLABUS, sections)

    assert len(analysis) == 8
    assert "communication" in analysis
    assert "critical_thinking" in analysis
    assert analysis["communication"]["score"] >= 20
    assert analysis["communication"]["level"] in {"Low", "Medium", "High"}
    assert analysis["communication"]["evidence"]
    evidence_item = analysis["communication"]["evidence"][0]
    assert "section" in evidence_item
    assert "excerpt" in evidence_item
    assert "reason" in evidence_item
    assert evidence_item["strength"] in {"Strong", "Moderate"}


def test_recommendation_and_render_pipeline():
    sections = split_into_sections(SAMPLE_SYLLABUS)
    recommendations = generate_recommendations(
        sections, ["communication", "technology"]
    )

    assert "communication" in recommendations
    assert "technology" in recommendations
    assert recommendations["communication"]["name"] == "Communication"
    assert recommendations["technology"]["name"] == "Technology"

    revised = render_revised_syllabus(
        SAMPLE_SYLLABUS,
        recommendations,
        course_name="Intro to Applied Analysis",
        course_code="ANLY 101",
        term="Fall 2026",
    )

    assert "Revised Syllabus Draft" in revised
    assert "[Communication] (communication)" in revised
    assert "ANLY 101 Intro to Applied Analysis" in revised
