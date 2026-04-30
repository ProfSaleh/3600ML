from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class CompetencyDefinition:
    name: str
    description: str
    indicators: List[str]
    placement_targets: List[str]
    light_template: str
    strong_template: str


COMPETENCIES: Dict[str, CompetencyDefinition] = {
    "career_self_development": CompetencyDefinition(
        name="Career & Self-Development",
        description="Self-awareness, growth mindset, and proactive career planning.",
        indicators=[
            "reflection",
            "self-assessment",
            "career goals",
            "professional development",
            "feedback",
            "improvement plan",
            "revision",
            "portfolio",
            "lifelong learning",
        ],
        placement_targets=["Learning Outcomes", "Weekly Activities", "Assignments"],
        light_template="Add a brief reflective checkpoint where students connect course learning to professional growth goals.",
        strong_template=(
            "Add a measurable outcome: 'Students will create and revise a professional development plan "
            "using instructor feedback and self-assessment evidence by week 10.'"
        ),
    ),
    "communication": CompetencyDefinition(
        name="Communication",
        description="Clear written, verbal, and digital communication for different audiences.",
        indicators=[
            "presentation",
            "writing",
            "written",
            "oral",
            "audience",
            "brief",
            "discussion post",
            "report",
            "communication rubric",
            "feedback",
        ],
        placement_targets=["Learning Outcomes", "Assignment Instructions", "Rubrics"],
        light_template="Clarify one assignment prompt with explicit audience and communication expectations.",
        strong_template=(
            "Add a measurable outcome: 'Students will deliver a discipline-appropriate communication artifact "
            "tailored to a specified audience and evaluated with a communication rubric.'"
        ),
    ),
    "critical_thinking": CompetencyDefinition(
        name="Critical Thinking",
        description="Analyze information, evaluate evidence, and solve complex problems.",
        indicators=[
            "analyze",
            "evaluate",
            "evidence",
            "argument",
            "problem-solving",
            "case study",
            "decision",
            "synthesis",
            "reasoning",
            "critique",
        ],
        placement_targets=["Learning Outcomes", "Assignments", "Assessments"],
        light_template="Add one prompt requiring students to evaluate competing evidence before making a conclusion.",
        strong_template=(
            "Add a measurable outcome: 'Students will analyze multiple evidence sources, justify decisions, "
            "and defend conclusions in written and oral formats.'"
        ),
    ),
    "equity_inclusion": CompetencyDefinition(
        name="Equity & Inclusion",
        description="Engage diverse perspectives and apply inclusive practices.",
        indicators=[
            "equity",
            "inclusion",
            "inclusive",
            "diversity",
            "bias",
            "cultural",
            "accessibility",
            "belonging",
            "marginalized",
            "perspective",
        ],
        placement_targets=["Course Policies", "Learning Outcomes", "Weekly Activities"],
        light_template="Add an activity where students compare diverse perspectives on a course issue.",
        strong_template=(
            "Add a measurable outcome: 'Students will evaluate how identity, context, and systemic bias affect "
            "disciplinary practice and propose inclusive responses.'"
        ),
    ),
    "leadership": CompetencyDefinition(
        name="Leadership",
        description="Influence and guide others ethically toward shared goals.",
        indicators=[
            "leadership",
            "initiative",
            "facilitate",
            "mentor",
            "coordinate",
            "delegate",
            "team lead",
            "ethics",
            "responsibility",
            "decision-making",
        ],
        placement_targets=["Group Project Instructions", "Learning Outcomes", "Rubrics"],
        light_template="Define one rotating facilitation role in group work with clear responsibilities.",
        strong_template=(
            "Add a measurable outcome: 'Students will demonstrate ethical leadership by planning team milestones, "
            "facilitating collaboration, and documenting impact on project outcomes.'"
        ),
    ),
    "professionalism": CompetencyDefinition(
        name="Professionalism",
        description="Reliable, ethical, and accountable professional behavior.",
        indicators=[
            "professionalism",
            "deadline",
            "attendance",
            "ethics",
            "accountability",
            "quality standards",
            "reliability",
            "work ethic",
            "conduct",
            "policy",
        ],
        placement_targets=["Course Policies", "Rubrics", "Assignments"],
        light_template="Add explicit quality and timeliness criteria to one graded assignment.",
        strong_template=(
            "Add a measurable outcome: 'Students will meet professional standards for timeliness, quality, and ethical "
            "practice as evaluated through rubric-based checkpoints.'"
        ),
    ),
    "teamwork": CompetencyDefinition(
        name="Teamwork",
        description="Collaborate effectively and resolve conflict to meet shared goals.",
        indicators=[
            "team",
            "collaborate",
            "group",
            "peer review",
            "conflict",
            "shared goals",
            "coordination",
            "co-author",
            "consensus",
            "peer feedback",
        ],
        placement_targets=["Group Assignments", "Rubrics", "Weekly Activities"],
        light_template="Add a peer-feedback checkpoint with shared team goals and role expectations.",
        strong_template=(
            "Add a measurable outcome: 'Students will collaborate in diverse teams, manage conflict constructively, "
            "and document contributions toward shared project goals.'"
        ),
    ),
    "technology": CompetencyDefinition(
        name="Technology",
        description="Use digital tools effectively, ethically, and responsibly.",
        indicators=[
            "technology",
            "digital",
            "software",
            "data",
            "platform",
            "analysis tool",
            "simulation",
            "ai",
            "security",
            "privacy",
        ],
        placement_targets=["Learning Outcomes", "Assignments", "Course Policies"],
        light_template="Specify one digital tool and expected workflow in an assignment description.",
        strong_template=(
            "Add a measurable outcome: 'Students will select and apply appropriate digital tools, interpret outputs, "
            "and explain ethical or privacy implications of their technology choices.'"
        ),
    ),
}


WEEKLY_KEYWORDS = (
    "week",
    "module",
    "unit",
    "assignment",
    "discussion",
    "dq",
    "quiz",
    "exam",
    "project",
    "lab",
    "presentation",
)

TASK_KEYWORDS = (
    "assignment",
    "discussion",
    "dq",
    "quiz",
    "exam",
    "project",
    "paper",
    "report",
    "presentation",
    "lab",
    "reflection",
)

WEEKLY_SOURCE_SECTIONS = {"Weekly Schedule", "Assignments", "Assessment"}

SECTION_PRIORITY = [
    "Weekly Schedule",
    "Assignments",
    "Assessment",
    "Learning Outcomes",
    "Course Description",
    "General",
    "Policies",
]


PLACEMENT_SECTION_MAP = {
    "Learning Outcomes": "Learning Outcomes",
    "Assignments": "Assignments",
    "Weekly Activities": "Weekly Schedule",
    "Weekly Schedule": "Weekly Schedule",
    "Assessments": "Assessment",
    "Assessment": "Assessment",
    "Course Policies": "Policies",
    "Policies": "Policies",
    "Assignment Instructions": "Assignments",
    "Rubrics": "Assessment",
    "Group Project Instructions": "Assignments",
    "Group Assignments": "Assignments",
}

EXEMPLAR_LIBRARY: Dict[str, dict] = {
    "career_self_development": {
        "strong_evidence_example": (
            "Week 5 Reflection: Students submit a professional growth memo, map two career "
            "goals, and revise the memo after instructor feedback using a reflection rubric."
        ),
        "suggestion_stem": (
            "Add a reflection checkpoint with revision criteria and require students to connect "
            "course performance to a professional development goal."
        ),
    },
    "communication": {
        "strong_evidence_example": (
            "Week 6 Policy Brief: Students produce a 2-page brief for a non-technical audience "
            "and present it in class, evaluated with communication rubric criteria."
        ),
        "suggestion_stem": (
            "Specify audience, message purpose, and rubric criteria for clarity, evidence use, "
            "and organization."
        ),
    },
    "critical_thinking": {
        "strong_evidence_example": (
            "Week 4 Case Analysis: Students evaluate two competing evidence sources, justify "
            "their decision, and defend trade-offs in a short written argument."
        ),
        "suggestion_stem": (
            "Require students to compare evidence options, justify choices, and explain trade-offs "
            "using explicit analysis criteria."
        ),
    },
    "equity_inclusion": {
        "strong_evidence_example": (
            "Week 7 Discussion: Students analyze how policy decisions affect diverse communities "
            "and propose inclusive alternatives with supporting evidence."
        ),
        "suggestion_stem": (
            "Prompt students to analyze impact across diverse groups and include an inclusion-focused "
            "evaluation criterion."
        ),
    },
    "leadership": {
        "strong_evidence_example": (
            "Project Milestone: Team leaders rotate weekly, document delegation decisions, and "
            "reflect on team outcomes using a leadership rubric."
        ),
        "suggestion_stem": (
            "Define rotating leadership roles, decision accountability, and team-impact reflection."
        ),
    },
    "professionalism": {
        "strong_evidence_example": (
            "Assignment Submission Policy: Work is evaluated for quality, timeliness, and professional "
            "standards with a transparent rubric."
        ),
        "suggestion_stem": (
            "Add explicit professional standards (timeliness, quality, ethical conduct) and grade "
            "against those standards."
        ),
    },
    "teamwork": {
        "strong_evidence_example": (
            "Week 8 Team Sprint: Students set shared goals, complete peer feedback, and submit "
            "a contribution log with conflict-resolution notes."
        ),
        "suggestion_stem": (
            "Require clear team roles, peer feedback, and contribution evidence to assess collaboration."
        ),
    },
    "technology": {
        "strong_evidence_example": (
            "Week 9 Data Task: Students use a digital analysis tool, interpret outputs, and document "
            "ethical/privacy implications in a short methods note."
        ),
        "suggestion_stem": (
            "Name the digital tool, expected workflow, and evaluation criteria for interpretation and "
            "ethical technology use."
        ),
    },
}

QUALITY_SIGNAL_TERMS = {
    "measurable_verb": ("analyze", "evaluate", "create", "design", "develop", "justify", "apply"),
    "deliverable": ("submit", "brief", "report", "memo", "presentation", "project", "quiz", "exam"),
    "assessment_criteria": ("rubric", "graded", "criteria", "points", "score"),
    "audience_or_context": ("audience", "client", "community", "stakeholder", "real-world"),
    "feedback_or_iteration": ("feedback", "revise", "peer review", "revision"),
}


def _score_from_hits(hit_count: int) -> str:
    if hit_count >= 6:
        return "High"
    if hit_count >= 3:
        return "Medium"
    return "Low"


def _numeric_score(hit_count: int) -> int:
    # Baseline + weighted indicator hits, capped at 95.
    return min(95, 20 + (hit_count * 9))


def _preview(text: str, max_len: int = 200) -> str:
    cleaned = " ".join(text.split())
    if len(cleaned) <= max_len:
        return cleaned
    return cleaned[: max_len - 3].rstrip() + "..."


def _split_evidence_units(text: str) -> List[str]:
    parts = re.split(r"(?<=[.!?])\s+|\n+", text)
    units: List[str] = []
    for part in parts:
        cleaned = part.strip(" -\t")
        if len(cleaned) >= 20:
            units.append(cleaned)
    return units


def _ordered_sections(sections: Dict[str, str]) -> List[tuple[str, str]]:
    seen = set()
    ordered: List[tuple[str, str]] = []
    for section_name in SECTION_PRIORITY:
        if section_name in sections:
            ordered.append((section_name, sections.get(section_name, "")))
            seen.add(section_name)
    for section_name, value in sections.items():
        if section_name not in seen:
            ordered.append((section_name, value))
    return ordered


def _strength_rank(label: str) -> int:
    if label == "Strong":
        return 3
    if label == "Moderate":
        return 2
    return 1


def _evidence_strength(match_count: int, excerpt: str) -> str:
    action_terms = (
        "students will",
        "assess",
        "evaluate",
        "analyze",
        "present",
        "create",
        "develop",
        "apply",
        "submit",
        "design",
        "collaborate",
        "reflect",
        "rubric",
        "graded",
    )
    excerpt_lc = excerpt.lower()
    has_action = any(term in excerpt_lc for term in action_terms)
    if match_count >= 2 or (match_count >= 1 and has_action):
        return "Strong"
    if match_count == 1:
        return "Moderate"
    return "Low"


def _extract_week_label(text: str) -> str | None:
    match = re.search(r"\b(week|module|unit)\s*\d+\b", text, flags=re.IGNORECASE)
    if match:
        return match.group(0).title()
    return None


def _source_type(section_name: str, excerpt: str) -> str:
    if section_name in WEEKLY_SOURCE_SECTIONS or _is_weekly_content(excerpt):
        return "weekly"
    if section_name in {"Learning Outcomes", "Course Description"}:
        return "course-level"
    return "general"


def _build_competency_evidence(
    competency: CompetencyDefinition, sections: Dict[str, str]
) -> tuple[int, List[str], List[dict]]:
    matched_indicators: List[str] = []
    evidence_pool: List[dict] = []
    seen_excerpts = set()

    for section_name, section_text in _ordered_sections(sections):
        if not section_text:
            continue
        for excerpt in _split_evidence_units(section_text):
            excerpt_lc = excerpt.lower()
            matches = [indicator for indicator in competency.indicators if indicator in excerpt_lc]
            if not matches:
                continue

            for indicator in matches:
                if indicator not in matched_indicators:
                    matched_indicators.append(indicator)

            preview = _preview(excerpt, 260)
            dedupe_key = (section_name, preview.lower())
            if dedupe_key in seen_excerpts:
                continue
            seen_excerpts.add(dedupe_key)

            strength = _evidence_strength(len(matches), excerpt)
            source = _source_type(section_name, excerpt)
            week_label = _extract_week_label(excerpt)
            evidence_pool.append(
                {
                    "section": section_name,
                    "excerpt": preview,
                    "indicator": matches[0],
                    "match_count": len(matches),
                    "strength": strength,
                    "source_type": source,
                    "week_label": week_label,
                    "reason": (
                        f"Mentions {len(matches)} competency keyword(s): {', '.join(matches[:3])}. "
                        f"Source priority: {source}."
                    ),
                }
            )

    evidence_pool.sort(
        key=lambda item: (_strength_rank(item["strength"]), item["match_count"]),
        reverse=True,
    )
    evidence = evidence_pool[:3]
    return len(matched_indicators), matched_indicators, evidence


def _is_weekly_content(excerpt: str) -> bool:
    excerpt_lc = excerpt.lower()
    return any(keyword in excerpt_lc for keyword in WEEKLY_KEYWORDS)


def _contains_task_marker(excerpt: str) -> bool:
    excerpt_lc = excerpt.lower()
    return any(keyword in excerpt_lc for keyword in TASK_KEYWORDS)


def _collect_weekly_lines(sections: Dict[str, str]) -> List[str]:
    weekly_lines: List[str] = []
    seen = set()
    for section_name in ("Weekly Schedule", "Assignments", "Assessment"):
        section_text = sections.get(section_name, "")
        if not section_text:
            continue
        for line in section_text.split("\n"):
            cleaned = line.strip(" -\t")
            if not cleaned:
                continue
            cleaned_lc = cleaned.lower()
            if cleaned_lc in seen:
                continue
            if section_name == "Weekly Schedule" or _contains_task_marker(cleaned):
                weekly_lines.append(cleaned)
                seen.add(cleaned_lc)
    return weekly_lines


def _collect_activity_lines(
    sections: Dict[str, str], assignment_mode: bool = False
) -> List[str]:
    activity_lines: List[str] = []
    seen = set()
    source_sections = ["Weekly Schedule", "Assignments", "Assessment"]
    if assignment_mode:
        source_sections.append("General")

    for section_name in source_sections:
        content = sections.get(section_name, "")
        if not content:
            continue
        for line in content.split("\n"):
            cleaned = line.strip(" -\t")
            if len(cleaned) < 12:
                continue
            lowered = cleaned.lower()
            if not (_contains_task_marker(lowered) or _is_weekly_content(lowered)):
                continue
            if lowered in seen:
                continue
            seen.add(lowered)
            activity_lines.append(cleaned)
    return activity_lines


def _weekly_overview(activity_lines: List[str], assignment_mode: bool) -> dict:
    if not activity_lines:
        if assignment_mode:
            summary = (
                "No clear assignment activity lines were detected. Include assignment prompt "
                "details, rubric criteria, or deliverable instructions to improve confidence."
            )
        else:
            summary = (
                "Weekly breakdown was not clearly detected. Add week-by-week assignment "
                "or activity lines (e.g., DQ, quiz, project milestone)."
            )
        return {
            "line_count": 0,
            "task_like_count": 0,
            "coverage": "Low",
            "summary": summary,
        }
    task_like = [line for line in activity_lines if _contains_task_marker(line)]
    if len(task_like) >= 6:
        coverage = "High"
    elif len(task_like) >= 3:
        coverage = "Medium"
    else:
        coverage = "Low"
    if assignment_mode:
        summary = (
            f"Detected {len(activity_lines)} assignment/activity lines; {len(task_like)} include "
            "concrete tasks (assignments, discussions, quizzes, exams, or projects)."
        )
    else:
        summary = (
            f"Detected {len(activity_lines)} weekly/activity lines; {len(task_like)} include "
            "concrete tasks (assignments, discussions, quizzes, exams, or projects)."
        )
    return {
        "line_count": len(activity_lines),
        "task_like_count": len(task_like),
        "coverage": coverage,
        "summary": summary,
    }


def _build_analysis_notes(
    sections: Dict[str, str], activity_lines: List[str], assignment_mode: bool
) -> dict:
    outcomes_present = bool(sections.get("Learning Outcomes", "").strip())
    description_present = bool(
        sections.get("Course Description", "").strip()
        or sections.get("General", "").strip()
    )
    weekly_present = bool(activity_lines)
    stage_2_summary = (
        "Primary scoring emphasis is based on assignment-level tasks (assignments, DQs, "
        "quizzes, exams, projects, rubrics, and instructions)."
        if assignment_mode
        else (
            "Primary scoring emphasis is based on weekly tasks (assignments, DQs, quizzes, "
            "exams, projects, labs, and presentations)."
        )
    )
    return {
        "stage_1": {
            "title": "Stage 1: Outcomes and course framing",
            "summary": (
                "Reviewed course outcomes/description first to identify declared learning goals."
            ),
            "outcomes_found": outcomes_present,
            "description_found": description_present,
        },
        "stage_2": {
            "title": "Stage 2: Weekly breakdown and task evidence",
            "summary": stage_2_summary,
            "weekly_found": weekly_present,
            "weekly_line_count": len(activity_lines),
        },
        "mode": "assignment" if assignment_mode else "syllabus",
    }


def _missing_explanation(
    hit_count: int, competency_name: str, assignment_mode: bool
) -> str:
    context = (
        "in this uploaded assignment artifact"
        if assignment_mode
        else "in this syllabus"
    )
    if hit_count == 0:
        return (
            f"No clear {competency_name} language was found {context}, so faculty may struggle "
            "to show where this skill is taught or assessed."
        )
    if hit_count <= 2:
        return (
            f"{competency_name} appears only in limited or implied ways. "
            "Students can benefit from explicit outcomes and assignment criteria."
        )
    return (
        f"{competency_name} has partial coverage but could be made easier to understand "
        "with clearer measurable language."
    )


def _focus_action(competency: CompetencyDefinition) -> str:
    return (
        f"Prioritize updates in: {', '.join(competency.placement_targets[:2])}. "
        "Add one measurable outcome and one assignment/rubric criterion."
    )


def _resolve_section(target_label: str) -> str:
    return PLACEMENT_SECTION_MAP.get(target_label, "General")


def _insertion_plan(target_label: str, sections: Dict[str, str]) -> dict:
    section_name = _resolve_section(target_label)
    section_text = sections.get(section_name, "").strip()
    if section_text:
        anchor = _preview(section_text.split("\n")[0], 120)
        return {
            "target_label": target_label,
            "section_name": section_name,
            "status": "Found existing section",
            "exact_location": (
                f"Go to the '{section_name}' section and add this near: \"{anchor}\"."
            ),
            "insertion_point": "Append as a new bullet near the end of the section.",
        }
    return {
        "target_label": target_label,
        "section_name": section_name,
        "status": "Section missing",
        "exact_location": (
            f"Create a '{section_name}' section and place this competency text there."
        ),
        "insertion_point": "Insert this section after course goals or assignment overview.",
    }


def _copy_ready_text(definition: CompetencyDefinition, target_label: str) -> str:
    if target_label == "Learning Outcomes":
        return f"Learning Outcome Addition: {definition.strong_template}"
    if target_label in {"Assignments", "Assignment Instructions", "Group Assignments"}:
        return f"Assignment Language Addition: {definition.light_template}"
    if target_label in {"Rubrics", "Assessment", "Assessments"}:
        return (
            "Rubric Criterion Addition: Add a criterion that directly evaluates this "
            f"competency. Suggested wording: {definition.light_template}"
        )
    if target_label in {"Course Policies", "Policies"}:
        return f"Policy/Expectation Addition: {definition.light_template}"
    return f"Suggested Addition: {definition.light_template}"


def evaluate_syllabus(
    _raw_text: str, sections: Dict[str, str], assignment_mode: bool = False
) -> Dict[str, dict]:
    results: Dict[str, dict] = {}
    activity_lines = _collect_activity_lines(sections, assignment_mode=assignment_mode)
    weekly_summary = _weekly_overview(activity_lines, assignment_mode=assignment_mode)
    analysis_notes = _build_analysis_notes(
        sections, activity_lines, assignment_mode=assignment_mode
    )
    activity_source_chunks = [
        sections.get("Weekly Schedule", ""),
        sections.get("Assignments", ""),
        sections.get("Assessment", ""),
    ]
    if assignment_mode:
        activity_source_chunks.append(sections.get("General", ""))
    weekly_activity_text_lc = "\n".join(
        [
            chunk for chunk in activity_source_chunks if chunk
        ]
    ).lower()

    for key, competency in COMPETENCIES.items():
        hits, matched_indicators, evidence = _build_competency_evidence(competency, sections)
        weekly_indicator_hits = sum(
            1 for indicator in competency.indicators if indicator in weekly_activity_text_lc
        )
        evidence_weekly_count = sum(
            1 for item in evidence if _is_weekly_content(item["excerpt"])
        )
        if assignment_mode:
            weighted_hits = hits + (weekly_indicator_hits * 2) + evidence_weekly_count
        else:
            weighted_hits = hits + weekly_indicator_hits + evidence_weekly_count
        weighted_hits = min(weighted_hits, len(competency.indicators))

        level = _score_from_hits(weighted_hits)
        score = _numeric_score(weighted_hits)
        missing = level == "Low"
        rationale = (
            f"Detected {hits} indicators overall and {weekly_indicator_hits} in "
            f"{'assignment activity lines' if assignment_mode else 'weekly breakdown'}, "
            f"resulting in a {level} coverage rating with activity emphasis."
        )
        if missing:
            rationale += " Coverage is weak or missing and needs explicit measurable language."

        confidence = "High" if weighted_hits >= 5 else "Medium" if weighted_hits >= 2 else "Low"
        weekly_priority_note = (
            f"Activity evidence matches for this competency: {evidence_weekly_count}. "
            "Add explicit assignment/assessment tasks if this is low."
        )

        results[key] = {
            "name": competency.name,
            "description": competency.description,
            "score": score,
            "level": level,
            "missing_or_weak": missing,
            "indicator_hits": weighted_hits,
            "raw_indicator_hits": hits,
            "weekly_indicator_hits": weekly_indicator_hits,
            "matched_indicators": matched_indicators,
            "confidence": confidence,
            "rationale": rationale,
            "missing_explanation": _missing_explanation(
                hits, competency.name, assignment_mode=assignment_mode
            ),
            "recommended_focus": _focus_action(competency),
            "weekly_priority_note": weekly_priority_note,
            "weekly_focus": {
                "has_weekly_items": bool(activity_lines),
                "weekly_lines_found": weekly_summary["line_count"],
                "activity_lines_found": weekly_summary["line_count"],
                "task_items_found": weekly_summary["task_like_count"],
                "competency_weekly_matches": evidence_weekly_count,
                "summary": weekly_summary["summary"],
            },
            "analysis_flow": analysis_notes,
            "analysis_mode": "assignment" if assignment_mode else "syllabus",
            "assignment_mode": assignment_mode,
            "evidence": evidence,
            "placement_targets": competency.placement_targets,
            "suggestions": {
                "light": competency.light_template,
                "strong": competency.strong_template,
            },
        }

    results["_analysis_meta"] = {
        "weekly_summary": weekly_summary,
        "analysis_notes": analysis_notes,
        "assignment_mode": assignment_mode,
    }
    return results


def generate_recommendations(
    sections: Dict[str, str], selected_competencies: List[str], assignment_mode: bool = False
) -> Dict[str, dict]:
    recommendations: Dict[str, dict] = {}
    activity_lines = _collect_activity_lines(sections, assignment_mode=assignment_mode)
    for key in selected_competencies:
        definition = COMPETENCIES[key]
        placements = []
        for target_label in definition.placement_targets:
            plan = _insertion_plan(target_label, sections)
            plan["copy_ready_text"] = _copy_ready_text(definition, target_label)
            placements.append(plan)
        weekly_task_suggestions: List[str] = []
        for line in activity_lines[:10]:
            if _contains_task_marker(line):
                weekly_task_suggestions.append(
                    f"{line}\nSuggested addition: {definition.light_template}"
                )
            if len(weekly_task_suggestions) >= 3:
                break
        if not weekly_task_suggestions:
            if assignment_mode:
                weekly_task_suggestions = [
                    "Add one assignment instruction that explicitly names this competency and how it will be graded.",
                    "Add one rubric row tied to this competency with clear performance criteria.",
                ]
            else:
                weekly_task_suggestions = [
                    "Add a weekly line such as: 'Week X: DQ on applying this competency to a real scenario.'",
                    "Add a graded milestone in weekly schedule tied to this competency.",
                ]
        recommendations[key] = {
            "name": definition.name,
            "placements": placements,
            "weekly_task_suggestions": weekly_task_suggestions,
            "why": (
                "These sections are where this competency is usually made explicit. "
                "Weekly tasks are prioritized so competency evidence is visible in day-to-day coursework."
            ),
            "light_edit": definition.light_template,
            "strong_edit": definition.strong_template,
        }
    return recommendations


def render_revised_syllabus(
    original_text: str,
    recommendations: Dict[str, dict],
    course_name: str,
    course_code: str,
    term: str,
) -> str:
    header = [
        "=== Revised Syllabus Draft (NACE Suggested Additions) ===",
        f"Course: {course_code} {course_name}".strip(),
        f"Term: {term}".strip(),
        "",
        "---- Suggested Competency Insertions ----",
    ]
    blocks: List[str] = []
    for competency_key, payload in recommendations.items():
        placement_lines = []
        for placement in payload["placements"]:
            placement_lines.append(
                f"- {placement['target_label']} -> {placement['exact_location']} "
                f"({placement['insertion_point']})"
            )
        placements = "\n".join(placement_lines)
        blocks.extend(
            [
                "",
                f"[{payload['name']}] ({competency_key})",
                "Recommended placement plan:",
                placements,
                f"Light edit: {payload['light_edit']}",
                f"Strong integration: {payload['strong_edit']}",
            ]
        )
    return "\n".join(header + blocks + ["", "---- Original Syllabus ----", original_text])


COMPETENCY_DEFS = {value.name: value for value in COMPETENCIES.values()}
