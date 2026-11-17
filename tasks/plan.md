# Implementation Plan: Streamline App & Remove Unnecessary Bloat

## Overview
Decompose the approved specification (`SPEC-streamline-app.md`) into small, independently verifiable tasks. The goal is to eliminate non-functional widgets, dead variable assignments, orphaned CSS rules, external CDN dependencies, and academic rubric clutter from `app.py`, as well as remove redundant duplicate PDFs from the repository root, ensuring 100% test pass rate and zero regressions.

---

## Architecture Decisions
1. **Preserve Tested Strings and Mode Identifiers**:
   - `tests/test_app.py` specifically tests for Certainty Factor badges, Doctor Prescribed Test boxes, Prescription plans, and mode switching to `"🔍 Cascading Decision-Tree Audit"`. All corresponding strings, structure, and callbacks will be strictly preserved.
2. **Remove Non-Functional Sidebar Inputs**:
   - `chassis_type` (Form Factor / Chassis dropdown) in `app.py` does nothing and is not referenced in inference or output. Removing it removes visual noise.
3. **Consolidate Navigation to Core User Modes**:
   - Mode 3 ("📚 Knowledge Base & 52 Conditions (Rubric Proof)") was created solely for an academic grading rubric checklist. Removing it leaves a clean 2-mode workflow:
     1. `⚡ Emergency Fast-Triage` (targeted symptom diagnosis)
     2. `🔍 Cascading Decision-Tree Audit` (systematic hardware checkup across all 7 domains)
4. **Decouple from External Remote Assets**:
   - Replace remote CDN image URL with native clean rendering / emoji to guarantee fast and reliable offline loading.
5. **Clean Root-Level Duplicate PDFs Safely**:
   - Delete the 2 root-level duplicate PDF reports (`CT_24263_Muhammad Afzal Iqbal_Lab_011_OOAD.pdf` and `Muhammad_Afzal_Iqbal_CT_24263_A_Expert_System_CCP.pdf`) while leaving their canonical copies in `docs/` intact.

---

## Dependency Graph
```text
SPEC-streamline-app.md
       │
       ├── Task 1: Clean dead code, unused widgets & orphaned CSS from app.py
       │       │
       │       └── Task 2: Streamline consultation modes in app.py (remove Mode 3)
       │               │
       │          [Checkpoint 1: Streamlit UI Clean & Passing]
       │               │
       ├── Task 3: Clean root duplicate files & update .gitignore
       │       │
       └── Task 4: Full regression verification & test suite run
               │
          [Checkpoint 2: Complete System Verification]
```

---

## Task List

### Phase 1: Streamlit UI Cleanup & Streamlining
- [ ] **Task 1: Clean Dead Code, Unused Widgets, and Orphaned CSS from `app.py`**
- [ ] **Task 2: Streamline Consultation Modes in `app.py` (Remove Academic Rubric Proof)**

### Checkpoint: Streamlit UI Clean & Passing
- [ ] `app.py` compiles cleanly without syntax warnings or errors.
- [ ] `tests/test_app.py` passes 100%.

### Phase 2: Repository Cleanup & Regression Verification
- [ ] **Task 3: Clean Repository Root Duplicate Files and Update `.gitignore`**
- [ ] **Task 4: Full Regression and Verification Suite**

### Checkpoint: Complete System Verification
- [ ] Working tree clean, duplicate PDFs removed, `scratch/` ignored.
- [ ] All 42 tests in `pytest` pass with 100% green status.

---

## Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Removing Mode 3 breaks session state or navigation tests | Medium | Verify `tests/test_app.py` does not reference Mode 3, and test mode switching between Triage and Audit after removal. |
| Removing CSS classes breaks existing layout | Low | Grepped and confirmed `.doctor-card`, `.prescription-box`, and `.test-box` are nowhere used in HTML/Markdown blocks in `app.py`. |
| Accidental deletion of original documents | High | Confirm canonical copies exist in `docs/` before deleting duplicate files from repository root. |

---

## Open Questions
- None. Scope and boundaries confirmed in `SPEC-streamline-app.md`.
