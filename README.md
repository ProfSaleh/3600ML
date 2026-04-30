# NACE Syllabus Assistant (MVP Prototype)

This repository now contains a working prototype app that helps faculty map and apply NACE competencies to a course syllabus.

## What the prototype does

The app implements the full 5-step MVP flow:

1. **Upload or paste a syllabus** (`.pdf`, `.docx`, `.txt`, or plain text)
2. **Analyze current coverage** across all 8 NACE competencies
3. **Show evidence and rationale** for each competency score
4. **Let faculty select competencies** to strengthen and generate placement suggestions
5. **Generate revised syllabus text** and export alignment outputs

## Tech stack

- Python 3.12+
- Streamlit
- `pypdf` (PDF text extraction)
- `python-docx` (DOCX text extraction)
- `pytest` (tests)

## Run locally

```bash
pip3 install -r requirements.txt
streamlit run app.py
```

Then open the local Streamlit URL printed in your terminal.

## Run tests

```bash
pytest -q
```

Current test suite covers:

- section parsing
- competency scoring pipeline
- recommendation generation + revised syllabus rendering
