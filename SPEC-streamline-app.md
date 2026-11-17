# Spec: Streamline App & Remove Unnecessary Bloat

## Objective
Clean up and streamline the LapDoc application and repository by eliminating dead code, unused UI widgets, redundant CSS, external network dependencies, academic grading clutter, and duplicate root-level files, while preserving 100% backward compatibility and test suite pass rate.

The user will experience a faster, cleaner, distraction-free diagnostic application without superficial sidebar inputs or academic rubric boilerplate.

---

## Tech Stack
- **Language**: Python 3.10+ (tested on Python 3.14)
- **Frameworks/Libraries**: Streamlit >= 1.30.0, Pandas >= 2.0.0, Pytest >= 8.0.0
- **Standard Library**: `os`, `json`, `dataclasses`, `typing`, `re`

---

## Commands
- **Run Test Suite**: `.venv/bin/pytest`
- **Run Streamlit Web App**: `.venv/bin/streamlit run app.py`
- **Run Terminal CLI**: `.venv/bin/python cli.py`
- **Run Syntax & Compilation Check**: `.venv/bin/python -m py_compile app.py cli.py engine.py`

---

## Project Structure
```text
laptop-expert-system/
├── app.py                      # Streamlit Web UI (streamlined: removed dead widgets, dead variables & unused CSS)
├── cli.py                      # Terminal CLI runner (unmodified)
├── engine.py                   # Core Inference Engine (unmodified)
├── knowledge_base.json         # Declarative Knowledge Base (unmodified)
├── docs/                       # Project documentation & preserved academic artifacts
│   ├── EXPERT_SYSTEM_EVALUATION.md
│   ├── CT_24263_Muhammad Afzal Iqbal_Lab_011_OOAD.pdf
│   └── Muhammad_Afzal_Iqbal_CT_24263_A_Expert_System_CCP.pdf
├── SPEC-streamline-app.md      # This specification
├── tests/                      # Automated test suite (must remain 100% passing)
│   ├── test_app.py
│   ├── test_boundary.py
│   ├── test_cli.py
│   ├── test_doctor_consultation.py
│   ├── test_engine.py
│   ├── test_knowledge_base.py
│   ├── test_tree_audit.py
│   └── test_uncertainty.py
└── .gitignore                  # Updated to ignore scratch/ and temporary artifacts
```

---

## Unnecessary Elements Identified & Remediation Scope

### 1. In `app.py`:
- **Dead Widget: Form Factor / Chassis Dropdown**
  - *Location*: Lines 107-110 in `app.py` (`chassis_type = st.selectbox(...)`).
  - *Issue*: Completely unused anywhere in the logic or UI.
  - *Action*: Remove this widget entirely.
- **Dead Variable: Unused Report Assignment**
  - *Location*: Line 190 in `app.py` (`report = engine.generate_doctor_report(...)`).
  - *Issue*: `report` is computed but never rendered or accessed in the script.
  - *Action*: Remove the unused assignment (or if kept, render or eliminate).
- **Orphaned CSS Classes**
  - *Location*: Lines 27-48 in `app.py` (`.doctor-card`, `.prescription-box`, `.test-box`).
  - *Issue*: These CSS classes are defined in `<style>` but never applied to any HTML/markdown element.
  - *Action*: Remove orphaned CSS rules to keep stylesheet lean and maintainable.
- **External Network Dependency for Sidebar Icon**
  - *Location*: Line 73 in `app.py` (`st.image("https://img.icons8.com/fluency/96/stethoscope.png", width=64)`).
  - *Issue*: Relies on third-party remote CDN. If offline or slow connection, causes visual degradation or delay.
  - *Action*: Replace with local clean rendering / native emoji icon header.
- **Academic Rubric Tab (Mode 3: "📚 Knowledge Base & 52 Conditions (Rubric Proof)")**
  - *Location*: Lines 519-587 in `app.py`.
  - *Issue*: Exposes university assignment grading rubric checklist ("5-Point Rubric Verification Checklist", "Exceeds Rubric delta", etc.) that is irrelevant and distracting for users running laptop diagnostics.
  - *Action*: Streamline mode selection to the 2 real user workflows:
    1. `⚡ Emergency Fast-Triage` (targeted symptom diagnosis)
    2. `🔍 Cascading Decision-Tree Audit` (systematic hardware checkup across all 7 domains)
    *(Optional: Keep knowledge base inspection in an expander or developer drawer if user desires, or cut entirely).*

### 2. In Repository Root:
- **Duplicate Root PDFs**
  - *Location*: `CT_24263_Muhammad Afzal Iqbal_Lab_011_OOAD.pdf` and `Muhammad_Afzal_Iqbal_CT_24263_A_Expert_System_CCP.pdf` in project root.
  - *Issue*: Redundant 2.2MB duplicate copies of files already preserved in `docs/`.
  - *Action*: Delete root duplicate PDFs and ensure `docs/` copies remain untouched.
- **Ignore Scratch Artifacts**
  - *Location*: `scratch/` directory.
  - *Issue*: Contains temporary scripts, images, and HTML dumps.
  - *Action*: Add `scratch/` and `*.pdf` (at root level) to `.gitignore`.

---

## Code Style
- **Python / Streamlit Best Practices**:
  - Keep sidebar focused and free of non-functional inputs.
  - Only declare UI widgets that actually alter state, filtering, or inference logic.
  - Clean inline CSS without orphaned class definitions.
  - Explicit typing and docstrings preserved on all modified functions.

---

## Testing Strategy
- **Framework**: `pytest` running in `.venv`.
- **Target**: All 42 existing tests must pass with zero failures:
  1. `tests/test_app.py` (App compilation, UI elements, button mode switch)
  2. `tests/test_boundary.py`
  3. `tests/test_cli.py`
  4. `tests/test_doctor_consultation.py`
  5. `tests/test_engine.py`
  6. `tests/test_knowledge_base.py`
  7. `tests/test_tree_audit.py`
  8. `tests/test_uncertainty.py`
- **Regression Guard**: All expected strings asserted by `test_app.py` (e.g., `"Doctor's Order: Prescribed Diagnostic Desk Test"`, `"Doctor's Prescription & Actionable Treatment Plan"`, `"Launch Full 50-Point Subsystem Audit"`, Certainty meters) must be preserved.

---

## Boundaries
- **Always**:
  - Run `.venv/bin/pytest` before and after all changes.
  - Ensure all 42 automated tests pass cleanly.
  - Preserve core expert system engine logic in `engine.py` and `knowledge_base.json`.
- **Ask First**:
  - If removing the entire 50-Point Subsystem Audit mode (currently preserving it as it is a core feature tested by `test_app.py`).
  - If changing the medical consultation terminology in `app.py` (currently preserved to maintain compatibility with `test_app.py`).
- **Never**:
  - Never remove features or strings expected by `tests/test_app.py`.
  - Never delete files from `docs/` without explicit instruction.
  - Never introduce external network requirements.

---

## Success Criteria
1. `app.py` contains zero unused inputs (`chassis_type` removed).
2. `app.py` contains zero dead variable assignments (`report = ...` cleaned up).
3. `app.py` stylesheet contains zero orphaned CSS classes.
4. Mode selection in `app.py` is streamlined (Mode 3 rubric proof removed or relocated out of primary user navigation).
5. External image URL replaced with reliable local/native rendering.
6. Root directory cleaned of duplicate 2.2MB PDFs, and `.gitignore` updated.
7. All 42 tests in `pytest` pass with 100% success.

---

## Open Questions
1. **Mode 3 (Academic Rubric Proof)**: Would you like Mode 3 completely removed from `app.py`, or retained under a collapsed "Developer / Audit Tools" expander in the sidebar?
2. **Device Profile (`brand` & `processor`)**: Currently `brand` and `processor` in the sidebar do not change the diagnostic reasoning in `engine.py` (they only customize the title banner and scorecard filename). Would you like to keep them for personalized reports, or remove them as well for an ultra-minimal UI?
3. **Medical Framing**: Do you want to keep the "Laptop Doctor" clinical consultation framing (which is verified by `tests/test_app.py`), or would you like to reframe it into traditional IT hardware terminology?
