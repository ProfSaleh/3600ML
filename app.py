from __future__ import annotations

from io import BytesIO
from typing import Dict, List

import streamlit as st

from nace_engine import (
    COMPETENCY_DEFS,
    evaluate_syllabus,
    generate_recommendations,
    render_revised_syllabus,
)
from parser import SectionMap, extract_text_from_upload, split_into_sections

st.set_page_config(page_title="NACE Syllabus Assistant", page_icon="🎓", layout="wide")

STEP_LABELS = {
    1: "1) Upload / Paste",
    2: "2) Scorecard",
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


def render_header() -> None:
    st.title("NACE Competency Syllabus Assistant (MVP)")
    st.caption(
        "Upload or paste a syllabus, review NACE competency coverage, select competencies, "
        "and apply suggested edits."
    )
    st.info("Current step: " + STEP_LABELS[st.session_state.step])


def parse_and_analyze(text: str) -> None:
    sections = split_into_sections(text)
    analysis = evaluate_syllabus(text, sections)
    st.session_state.syllabus_text = text
    st.session_state.sections = sections
    st.session_state.analysis = analysis
    st.session_state.recommendations = {}
    st.session_state.selected_competencies = []


def step_1_upload() -> None:
    st.subheader("Step 1: Upload or paste syllabus")
    left, right = st.columns(2)
    with left:
        st.session_state.course_name = st.text_input("Course Name", st.session_state.course_name)
        st.session_state.course_code = st.text_input("Course Code", st.session_state.course_code)
        st.session_state.term = st.text_input("Term", st.session_state.term)
        uploaded = st.file_uploader("Upload syllabus", type=["pdf", "docx", "txt"])
    with right:
        pasted = st.text_area(
            "Or paste syllabus text",
            value=st.session_state.syllabus_text,
            height=260,
            placeholder="Paste syllabus content here...",
        )

    if st.button("Analyze syllabus", type="primary"):
        text = ""
        if uploaded is not None:
            text = extract_text_from_upload(uploaded.name, uploaded.getvalue())
        elif pasted.strip():
            text = pasted

        if not text.strip():
            st.error("Please upload a file or paste text.")
            return

        parse_and_analyze(text)
        st.success("Analysis complete.")
        go_to_step(2)
        st.rerun()

    if st.session_state.syllabus_text:
        with st.expander("Preview extracted syllabus text", expanded=False):
            st.text_area("Extracted text", st.session_state.syllabus_text, height=240, disabled=True)


def step_2_scorecard() -> None:
    if not st.session_state.analysis:
        st.warning("No analysis available. Complete Step 1 first.")
        return

    st.subheader("Step 2: NACE competency scorecard")
    analysis: Dict[str, dict] = st.session_state.analysis
    cols = st.columns(2)
    for idx, (name, result) in enumerate(analysis.items()):
        with cols[idx % 2]:
            level = result["level"]
            score = result["score"]
            status = "Missing / Weak" if level == "Low" else "Present"
            st.markdown(
                f"### {score_color(level)} {name}\n"
                f"- **Score:** {score}/100 (**{level}**)\n"
                f"- **Status:** {status}\n"
                f"- **Confidence:** {result['confidence']}"
            )
            st.caption(result["rationale"])

    missing = [k for k, v in analysis.items() if v["level"] == "Low"]
    if missing:
        st.error("Missing/weak competencies: " + ", ".join(missing))
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

    st.subheader("Step 3: Evidence + rationale + select competencies")
    analysis: Dict[str, dict] = st.session_state.analysis
    selections: List[str] = []

    for competency, result in analysis.items():
        with st.container(border=True):
            st.markdown(f"### {competency} — {result['level']} ({result['score']}/100)")
            st.write(result["rationale"])
            st.markdown("**Evidence found**")
            if result["evidence"]:
                for snippet in result["evidence"]:
                    st.markdown(f"- `{snippet}`")
            else:
                st.markdown("- No direct evidence found.")
            if st.checkbox(
                f"Select {competency} for improvement",
                value=competency in st.session_state.selected_competencies,
                key=f"select_{competency}",
            ):
                selections.append(competency)

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
            )
            go_to_step(4)
            st.rerun()


def step_4_recommendations() -> None:
    if not st.session_state.recommendations:
        st.warning("No suggestions generated yet. Complete Step 3 first.")
        return

    st.subheader("Step 4: Placement recommendations")
    st.caption("Each competency has target sections, a light edit, and a stronger integration option.")
    recommendations: Dict[str, dict] = st.session_state.recommendations

    for competency, payload in recommendations.items():
        with st.container(border=True):
            st.markdown(f"### {competency}")
            st.markdown("**Best placement locations**")
            for i, location in enumerate(payload["placements"], start=1):
                st.markdown(f"{i}. {location}")
            st.markdown(f"**Why this location:** {payload['why']}")
            st.markdown("**Light edit**")
            payload["light_edit"] = st.text_area(
                f"{competency} light edit",
                value=payload["light_edit"],
                key=f"light_{competency}",
                height=90,
            )
            st.markdown("**Strong integration**")
            payload["strong_edit"] = st.text_area(
                f"{competency} strong edit",
                value=payload["strong_edit"],
                key=f"strong_{competency}",
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
    for competency, result in st.session_state.analysis.items():
        report_rows.append(
            {
                "competency": competency,
                "score": result["score"],
                "level": result["level"],
                "selected_for_improvement": competency in st.session_state.selected_competencies,
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
