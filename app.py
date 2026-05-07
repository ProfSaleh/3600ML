from __future__ import annotations

from typing import Dict, List

import streamlit as st

from nace_engine import (
    evaluate_syllabus,
    generate_recommendations,
    render_revised_syllabus,
)
from parser import extract_text_from_upload, split_into_sections

st.set_page_config(page_title="NACE Assignment Assistant", page_icon="🎓", layout="wide")

STEP_LABELS = {
    1: "1) Upload Assignment",
    2: "2) Analysis Scorecard",
    3: "3) Evidence + Select",
    4: "4) Placement Suggestions",
    5: "5) Review + Export",
}


def init_state() -> None:
    defaults = {
        "step": 1,
        "syllabus_text": "",
        "sections": {},
        "analysis": {},
        "selected_competencies": [],
        "recommendations": {},
        "course_name": "",
        "course_code": "",
        "term": "",
        "assignment_mode": True,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def go_to_step(step: int) -> None:
    st.session_state.step = step


def score_color(level: str) -> str:
    if level == "High":
        return "🟢"
    if level == "Medium":
        return "🟡"
    return "🔴"


def score_badge(level: str, score: int) -> str:
    return f"{score_color(level)} {level} ({score}/100)"


def evidence_strength_badge(strength: str) -> str:
    if strength == "Strong":
        return "🟢 Strong"
    if strength == "Moderate":
        return "🟡 Moderate"
    return "🔵 Supporting"


def evidence_card_style(strength: str) -> str:
    if strength == "Strong":
        return "🟢"
    if strength == "Moderate":
        return "🟡"
    return "🔵"


def render_header() -> None:
    st.title("NACE Competency Assignment Assistant")
    st.caption(
        "Upload or paste an assignment, analyze where NACE competencies are covered or missing, "
        "and get realistic assignment-aligned rewrites."
    )
    st.info("Current step: " + STEP_LABELS[st.session_state.step])


def parse_and_analyze(text: str) -> None:
    sections = split_into_sections(text)
    analysis = evaluate_syllabus(
        text,
        sections,
        assignment_mode=st.session_state.assignment_mode,
    )
    st.session_state.syllabus_text = text
    st.session_state.sections = sections
    st.session_state.analysis = analysis
    st.session_state.recommendations = {}
    st.session_state.selected_competencies = []


def assessment_focus_badge(source: str) -> str:
    if source == "weekly":
        return "🗓️ Weekly/assignment/assessment evidence (primary)"
    if source == "foundational":
        return "📘 Course outcomes/description evidence"
    return "📄 General syllabus evidence"


def step_1_upload() -> None:
    st.subheader("Step 1: Upload or paste assignment")
    left, right = st.columns(2)
    with left:
        st.session_state.course_name = st.text_input("Course Name", st.session_state.course_name)
        st.session_state.course_code = st.text_input("Course Code", st.session_state.course_code)
        st.session_state.term = st.text_input("Term", st.session_state.term)
        st.session_state.assignment_mode = st.toggle(
            "Assignment Mode (single assignment upload)",
            value=st.session_state.assignment_mode,
            help=(
                "Use this when uploading one assignment instead of a full syllabus. "
                "Scoring will prioritize assignment/rubric content and avoid penalizing "
                "missing syllabus-wide sections."
            ),
        )
        uploaded = st.file_uploader("Upload assignment", type=["pdf", "docx", "txt"])
    with right:
        pasted = st.text_area(
            "Or paste assignment text",
            value=st.session_state.syllabus_text,
            height=260,
            placeholder="Paste assignment content here...",
        )

    if st.button("Analyze Assignment", type="primary"):
        text = ""
        if uploaded is not None:
            text = extract_text_from_upload(uploaded.name, uploaded.getvalue())
        elif pasted.strip():
            text = pasted

        if not text.strip():
            st.error("Please upload a file or paste text.")
            return

        with st.spinner("Analyzing assignment evidence and competency coverage..."):
            parse_and_analyze(text)
        st.success("Assignment analysis complete.")
        go_to_step(2)
        st.rerun()

    if st.session_state.syllabus_text:
        with st.expander("Preview extracted assignment text", expanded=False):
            st.text_area("Extracted text", st.session_state.syllabus_text, height=240, disabled=True)


def step_2_scorecard() -> None:
    if not st.session_state.analysis:
        st.warning("No analysis available. Complete Step 1 first.")
        return

    st.subheader("Step 2: Assignment competency scorecard")
    analysis: Dict[str, dict] = st.session_state.analysis
    meta = analysis.get("_analysis_meta", {})
    stage_notes = meta.get("analysis_notes", {})
    weekly_summary = meta.get("weekly_summary", {})
    if stage_notes:
        st.markdown("### How this analysis was performed")
        stage1 = stage_notes.get("stage_1", {})
        stage2 = stage_notes.get("stage_2", {})
        st.info(
            f"1) {stage1.get('summary', '')}\n\n"
            f"2) {stage2.get('summary', '')}"
        )
    if weekly_summary:
        coverage = weekly_summary.get("coverage", "Low")
        coverage_badge = (
            "🟢 Weekly task detail is strong"
            if coverage == "High"
            else "🟡 Weekly task detail is moderate"
            if coverage == "Medium"
            else "🔴 Weekly task detail is weak"
        )
        st.caption(coverage_badge + f" — {weekly_summary.get('summary', '')}")

    competency_items = [
        (key, value)
        for key, value in analysis.items()
        if not key.startswith("_")
    ]
    evidence_total = sum(len(item[1].get("evidence", [])) for item in competency_items)
    covered_count = sum(1 for _, item in competency_items if item["level"] != "Low")
    missing_count = sum(1 for _, item in competency_items if item["level"] == "Low")
    avg_score = (
        round(sum(item["score"] for _, item in competency_items) / len(competency_items))
        if competency_items
        else 0
    )
    metric_cols = st.columns(4)
    metric_cols[0].metric("Assignment lines analyzed", weekly_summary.get("line_count", 0))
    metric_cols[1].metric("Evidence snippets", evidence_total)
    metric_cols[2].metric("Competencies covered", covered_count)
    metric_cols[3].metric("Avg competency score", f"{avg_score}/100")
    st.caption(f"Missing/weak competencies: {missing_count}")

    cols = st.columns(2)
    for idx, (name, result) in enumerate(competency_items):
        with cols[idx % 2]:
            level = result["level"]
            score = result["score"]
            coverage_status = "Missing / Weak" if level == "Low" else "Present"
            st.markdown(
                f"### {result['name']}\n"
                f"- **Status:** {score_badge(level, score)}\n"
                f"- **Coverage:** {coverage_status}\n"
                f"- **Confidence:** {result['confidence']}"
            )
            st.caption(result["description"])
            covered_sections = result.get("covered_sections", [])
            if covered_sections:
                st.caption("Evidence sections: " + ", ".join(covered_sections))
            else:
                st.caption("No assignment section evidence detected yet.")
            if result["missing_or_weak"]:
                st.warning(result["missing_explanation"], icon="⚠️")
            else:
                st.success("This competency has clear evidence in your assignment.")

    missing = [v["name"] for _, v in competency_items if v["level"] == "Low"]
    if missing:
        st.error(
            "Competencies that need attention: " + ", ".join(missing),
            icon="🚩",
        )
    else:
        st.success("No competencies currently flagged as low.")

    c1, c2 = st.columns([1, 1])
    with c1:
        if st.button("Back to Step 1"):
            go_to_step(1)
            st.rerun()
    with c2:
        if st.button("Review evidence", type="primary"):
            go_to_step(3)
            st.rerun()


def step_3_evidence_select() -> None:
    if not st.session_state.analysis:
        st.warning("No analysis available. Complete Step 1 first.")
        return

    st.subheader("Step 3: Assignment evidence + select competencies")
    analysis: Dict[str, dict] = st.session_state.analysis
    selections: List[str] = st.session_state.selected_competencies[:]

    competency_items = [
        (key, value)
        for key, value in analysis.items()
        if not key.startswith("_")
    ]
    for competency_key, result in competency_items:
        competency_name = result["name"]
        with st.container(border=True):
            st.markdown(f"### {competency_name}")
            st.markdown(f"**Coverage:** {score_badge(result['level'], result['score'])}")
            st.write(result["missing_explanation"])
            weekly_focus = result.get("weekly_focus", {})
            if weekly_focus:
                st.markdown(
                    f"**Weekly-first assessment:** {weekly_focus.get('summary', '')}"
                )
            if result.get("great_examples"):
                with st.expander("What strong evidence looks like", expanded=False):
                    for sample in result["great_examples"]:
                        st.code(sample, language="text")
            st.markdown("**Evidence found**")
            if result["evidence"]:
                for idx, evidence in enumerate(result["evidence"], start=1):
                    st.markdown(
                        f"{idx}. {evidence_card_style(evidence['strength'])} **Section:** `{evidence['section']}` "
                        f"| **Matched term:** `{evidence['indicator']}` "
                        f"| **Strength:** {evidence_strength_badge(evidence['strength'])}"
                    )
                    st.markdown(
                        f"   - **Source priority:** {assessment_focus_badge(evidence.get('source_type', 'general'))}"
                    )
                    st.markdown(
                        f"   - **Why this matters:** {evidence['reason']}"
                    )
                    st.markdown(
                        f"   - **Quality diagnostics:** {evidence.get('quality_diagnostics', 'N/A')}"
                    )
                    if evidence.get("quality_gap"):
                        st.markdown(f"   - **Quality gap to improve:** {evidence['quality_gap']}")
                    st.code(evidence["excerpt"], language="text")
                    if evidence.get("assignment_aligned_suggestion"):
                        st.markdown("   - **Suggested revision for this exact line:**")
                        st.code(evidence["assignment_aligned_suggestion"], language="text")
                    if evidence.get("great_example_reference"):
                        st.markdown("   - **Great example to emulate:**")
                        st.code(evidence["great_example_reference"], language="text")
            else:
                st.markdown("- No direct evidence found in this assignment text.")
            selected = st.checkbox(
                f"Select {competency_name} for improvement",
                value=competency_key in st.session_state.selected_competencies,
                key=f"select_{competency_key}",
                help="Select competencies you want placement-ready edits for.",
            )
            if selected and competency_key not in selections:
                selections.append(competency_key)
            if not selected and competency_key in selections:
                selections.remove(competency_key)

    st.session_state.selected_competencies = selections
    c1, c2 = st.columns([1, 1])
    with c1:
        if st.button("Back to Scorecard"):
            go_to_step(2)
            st.rerun()
    with c2:
        if st.button("Generate suggestions", type="primary"):
            if not selections:
                st.error("Select at least one competency.")
                return
            st.session_state.recommendations = generate_recommendations(
                st.session_state.sections,
                selections,
                assignment_mode=st.session_state.assignment_mode,
                analysis=st.session_state.analysis,
            )
            go_to_step(4)
            st.rerun()


def step_4_recommendations() -> None:
    if not st.session_state.recommendations:
        st.warning("No suggestions generated yet. Complete Step 3 first.")
        return

    st.subheader("Step 4: Assignment-aligned recommendations")
    st.caption(
        "Each competency below includes realistic, assignment-relative rewrites grounded in your uploaded content."
    )
    recommendations: Dict[str, dict] = st.session_state.recommendations

    for competency_key, payload in recommendations.items():
        with st.container(border=True):
            st.markdown(f"### {payload['name']}")
            st.markdown(
                f"**Recommendation confidence:** {payload.get('recommendation_confidence', 'N/A')}"
            )
            if payload.get("realism_note"):
                st.caption(payload["realism_note"])
            if payload.get("covered_sections"):
                st.caption("Grounded sections: " + ", ".join(payload["covered_sections"]))
            st.markdown("**Where to place this competency (exact plan)**")
            for i, placement in enumerate(payload["placements"], start=1):
                status_emoji = "✅" if placement["status"] == "Found existing section" else "➕"
                st.markdown(
                    f"{i}. {status_emoji} **{placement['target_label']}** "
                    f"→ Section: `{placement['section_name']}`"
                )
                st.markdown(f"   - **Instruction:** {placement['exact_location']}")
                st.markdown(f"   - **Insertion point:** {placement['insertion_point']}")
                st.markdown(f"   - **Copy-ready text:**")
                st.code(placement["copy_ready_text"], language="text")
            st.markdown(f"**Why this location:** {payload['why']}")
            if payload.get("weekly_task_suggestions"):
                st.markdown("**Assignment-aligned suggestions (priority)**")
                for weekly_suggestion in payload["weekly_task_suggestions"]:
                    st.code(weekly_suggestion, language="text")
            if payload.get("aligned_suggestions"):
                st.markdown("**Directly aligned rewrites (from your assignment lines)**")
                for aligned in payload["aligned_suggestions"]:
                    st.markdown(
                        f"- **Source line:** `{aligned['source_location']}`"
                    )
                    st.code(aligned["original_excerpt"], language="text")
                    st.markdown("  **Improved rewrite:**")
                    st.code(aligned["suggested_rewrite"], language="text")
                    st.caption(aligned["alignment_reason"])
                    if aligned.get("missing_signal_prompts"):
                        st.markdown(
                            "  **To make this even stronger:** "
                            + "; ".join(aligned["missing_signal_prompts"])
                        )
            if payload.get("great_example_reference"):
                st.markdown("**Great example to emulate**")
                st.code(payload["great_example_reference"], language="text")
            if payload.get("exemplar_rewrites"):
                st.markdown("**Exemplar-driven rewrites (assignment-ready)**")
                for rewrite in payload["exemplar_rewrites"]:
                    st.code(rewrite, language="text")
            st.markdown("**Light edit**")
            payload["light_edit"] = st.text_area(
                f"{competency_key} light edit",
                value=payload["light_edit"],
                key=f"light_{competency_key}",
                height=90,
            )
            st.markdown("**Strong integration**")
            payload["strong_edit"] = st.text_area(
                f"{competency_key} strong edit",
                value=payload["strong_edit"],
                key=f"strong_{competency_key}",
                height=120,
            )

    c1, c2 = st.columns([1, 1])
    with c1:
        if st.button("Back to Evidence"):
            go_to_step(3)
            st.rerun()
    with c2:
        if st.button("Review + export", type="primary"):
            st.session_state.recommendations = recommendations
            go_to_step(5)
            st.rerun()


def step_5_review_export() -> None:
    if not st.session_state.recommendations:
        st.warning("No recommendations available. Complete Step 4 first.")
        return

    st.subheader("Step 5: Review, apply, and export")
    revised_text = render_revised_syllabus(
        st.session_state.syllabus_text,
        st.session_state.recommendations,
        st.session_state.course_name,
        st.session_state.course_code,
        st.session_state.term,
    )

    with st.expander("Original syllabus", expanded=False):
        st.text_area("Original", st.session_state.syllabus_text, height=220, disabled=True)
    with st.expander("Revised syllabus with suggested insertions", expanded=True):
        st.text_area("Revised", revised_text, height=280)

    report_rows = []
    for competency_key, result in st.session_state.analysis.items():
        if competency_key.startswith("_"):
            continue
        report_rows.append(
            {
                "competency": result["name"],
                "score": result["score"],
                "level": result["level"],
                "selected_for_improvement": competency_key in st.session_state.selected_competencies,
                "missing_summary": result["missing_explanation"],
            }
        )
    st.markdown("### NACE alignment summary")
    st.dataframe(report_rows, use_container_width=True)

    st.download_button(
        "Download revised syllabus (.txt)",
        data=revised_text.encode("utf-8"),
        file_name="revised_syllabus.txt",
        mime="text/plain",
    )
    report_text = "\n".join(
        [
            "NACE Alignment Summary",
            f"Course: {st.session_state.course_code} {st.session_state.course_name}".strip(),
            f"Term: {st.session_state.term}".strip(),
            "",
        ]
        + [
            f"- {row['competency']}: {row['score']}/100 ({row['level']}) | "
            f"Selected: {row['selected_for_improvement']}"
            for row in report_rows
        ]
    )
    st.download_button(
        "Download alignment summary (.txt)",
        data=report_text.encode("utf-8"),
        file_name="nace_alignment_summary.txt",
        mime="text/plain",
    )

    c1, c2 = st.columns([1, 1])
    with c1:
        if st.button("Back to Suggestions"):
            go_to_step(4)
            st.rerun()
    with c2:
        if st.button("Start new analysis"):
            for k in [
                "syllabus_text",
                "sections",
                "analysis",
                "selected_competencies",
                "recommendations",
            ]:
                st.session_state[k] = "" if k == "syllabus_text" else {}
            st.session_state.selected_competencies = []
            go_to_step(1)
            st.rerun()


def main() -> None:
    init_state()
    render_header()

    if st.session_state.step == 1:
        step_1_upload()
    elif st.session_state.step == 2:
        step_2_scorecard()
    elif st.session_state.step == 3:
        step_3_evidence_select()
    elif st.session_state.step == 4:
        step_4_recommendations()
    elif st.session_state.step == 5:
        step_5_review_export()


if __name__ == "__main__":
    main()
