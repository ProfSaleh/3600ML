import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from nace_engine import evaluate_syllabus, generate_recommendations, render_revised_syllabus
from parser import parse_line_items, split_into_sections


SAMPLE_SYLLABUS = """
Course Objectives:
Students will analyze case studies and present findings to varied audiences.

Assignments:
Group project with peer review and final written report.

Weekly Schedule:
Week 4: Team facilitation and reflection checkpoint.
Week 5 Assignment: Submit policy memo with audience-specific communication.
Week 6 DQ: Critique two sources and respond to classmates with evidence.
Week 7 Quiz: Data interpretation and digital tool selection.
Week 8 Project Milestone: Team leadership rotation and progress update.

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


def test_parse_line_items_tracks_line_numbers_and_sections():
    line_items = parse_line_items(SAMPLE_SYLLABUS)
    assert line_items
    first = line_items[0]
    assert first["line_number"] >= 1
    assert first["section"] in {
        "Learning Outcomes",
        "Assignments",
        "Weekly Schedule",
        "Assessment",
        "General",
    }
    assert first["text"]


def test_evaluate_syllabus_returns_all_competencies():
    sections = split_into_sections(SAMPLE_SYLLABUS)
    analysis = evaluate_syllabus(SAMPLE_SYLLABUS, sections)

    assert len([k for k in analysis.keys() if not k.startswith("_")]) == 8
    assert "communication" in analysis
    assert "critical_thinking" in analysis
    assert analysis["communication"]["score"] >= 20
    assert analysis["communication"]["level"] in {"Low", "Medium", "High"}
    assert analysis["communication"]["evidence"]
    assert analysis["communication"]["weekly_focus"]["has_weekly_items"] is True
    assert "week" in analysis["communication"]["weekly_focus"]["summary"].lower()
    assert analysis["communication"]["weekly_focus"]["task_items_found"] >= 4
    assert analysis["communication"]["weekly_indicator_hits"] >= 1
    assert analysis["communication"]["covered_line_numbers"]
    assert analysis["_analysis_meta"]["line_by_line_scan"]["non_empty_lines"] > 0
    evidence_item = analysis["communication"]["evidence"][0]
    assert "section" in evidence_item
    assert "line_number" in evidence_item
    assert evidence_item["line_number"] > 0
    assert "line_reference" in evidence_item
    assert evidence_item["line_reference"].startswith("Line ")
    assert "excerpt" in evidence_item
    assert "reason" in evidence_item
    assert "quality_signals" in evidence_item
    assert "quality_gap" in evidence_item
    assert "missing_signal_examples" in evidence_item
    assert evidence_item["strength"] in {"Strong", "Moderate"}
    assert evidence_item["source_type"] in {"weekly", "course-level"}
    assert "great_examples" in analysis["communication"]
    assert analysis["communication"]["great_examples"]


def test_recommendation_and_render_pipeline():
    sections = split_into_sections(SAMPLE_SYLLABUS)
    analysis = evaluate_syllabus(SAMPLE_SYLLABUS, sections)
    recommendations = generate_recommendations(
        sections, ["communication", "technology"], analysis=analysis
    )

    assert "communication" in recommendations
    assert "technology" in recommendations
    assert recommendations["communication"]["name"] == "Communication"
    assert recommendations["technology"]["name"] == "Technology"
    assert recommendations["communication"]["weekly_task_suggestions"]
    assert recommendations["communication"]["exemplar_rewrites"]
    assert recommendations["communication"]["recommendation_confidence"] in {"Low", "Medium", "High"}
    assert recommendations["communication"]["realism_note"]
    assert recommendations["communication"]["covered_sections"]
    assert recommendations["communication"]["covered_line_numbers"]

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


def test_assignment_mode_does_not_penalize_missing_syllabus_sections():
    assignment_text = """
    Project 2: Community Impact Proposal
    Instructions:
    - Submit a written brief for a public audience.
    - Week 3 DQ: Peer review two proposals and provide actionable feedback.
    - Week 4 Quiz: Evaluate evidence quality and data interpretation.
    - Final project presentation with rubric-based grading.
    """
    sections = split_into_sections(assignment_text)
    analysis = evaluate_syllabus(assignment_text, sections, assignment_mode=True)

    assert analysis["communication"]["assignment_mode"] is True
    assert analysis["_analysis_meta"]["assignment_mode"] is True
    assert analysis["communication"]["score"] >= 35
    assert analysis["communication"]["great_examples"]


def test_suggestions_are_aligned_to_assignment_lines():
    assignment_text = """
    Assignment: Policy Communication Memo
    - Submit a 2-page memo for a community audience.
    - Quiz: Evaluate evidence reliability and explain your decision.
    - DQ: Provide peer feedback on two classmates' drafts.
    """
    sections = split_into_sections(assignment_text)
    analysis = evaluate_syllabus(assignment_text, sections, assignment_mode=True)
    recommendations = generate_recommendations(
        sections, ["communication"], assignment_mode=True, analysis=analysis
    )

    rewrites = recommendations["communication"]["aligned_suggestions"]
    assert rewrites
    assert "source_location" in rewrites[0]
    assert "Line " in rewrites[0]["source_location"]
    assert "suggested_rewrite" in rewrites[0]
    assert "apply_location" in rewrites[0]
    assert "missing_signal_prompts" in rewrites[0]
    assert rewrites[0]["alignment_reason"]
