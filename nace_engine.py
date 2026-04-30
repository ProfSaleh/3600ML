from __future__ import annotations

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


def _missing_explanation(hit_count: int, competency_name: str) -> str:
    if hit_count == 0:
        return (
            f"No clear {competency_name} language was found, so faculty may struggle "
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


def evaluate_syllabus(_raw_text: str, sections: Dict[str, str]) -> Dict[str, dict]:
    full_text = "\n".join(sections.values()).lower()
    section_lc = {name: content.lower() for name, content in sections.items()}
    section_original = {name: content for name, content in sections.items()}

    results: Dict[str, dict] = {}

    for key, competency in COMPETENCIES.items():
        hits = 0
        matched_indicators: List[str] = []
        evidence: List[str] = []

        for indicator in competency.indicators:
            if indicator in full_text:
                hits += 1
                matched_indicators.append(indicator)
                if len(evidence) < 3:
                    for section_name, content in section_lc.items():
                        if indicator in content:
                            original_snippet = section_original[section_name]
                            evidence.append(
                                f"[{section_name}] indicator '{indicator}': {_preview(original_snippet)}"
                            )
                            break

        level = _score_from_hits(hits)
        score = _numeric_score(hits)
        missing = level == "Low"
        rationale = (
            f"Detected {hits} competency indicators ({', '.join(matched_indicators[:5]) or 'none found'}), "
            f"which maps to a {level} coverage rating."
        )
        if missing:
            rationale += " Coverage is weak or missing and needs explicit measurable language."

        confidence = "High" if hits >= 5 else "Medium" if hits >= 2 else "Low"

        results[key] = {
            "name": competency.name,
            "description": competency.description,
            "score": score,
            "level": level,
            "missing_or_weak": missing,
            "indicator_hits": hits,
            "matched_indicators": matched_indicators,
            "confidence": confidence,
            "rationale": rationale,
            "missing_explanation": _missing_explanation(hits, competency.name),
            "recommended_focus": _focus_action(competency),
            "evidence": evidence,
            "placement_targets": competency.placement_targets,
            "suggestions": {
                "light": competency.light_template,
                "strong": competency.strong_template,
            },
        }

    return results


def generate_recommendations(
    sections: Dict[str, str], selected_competencies: List[str]
) -> Dict[str, dict]:
    recommendations: Dict[str, dict] = {}
    for key in selected_competencies:
        definition = COMPETENCIES[key]
        placements = []
        for target_label in definition.placement_targets:
            plan = _insertion_plan(target_label, sections)
            plan["copy_ready_text"] = _copy_ready_text(definition, target_label)
            placements.append(plan)
        recommendations[key] = {
            "name": definition.name,
            "placements": placements,
            "why": (
                "These sections are where this competency is usually made explicit "
                "and assessable in a syllabus."
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
