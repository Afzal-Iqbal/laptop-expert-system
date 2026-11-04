# Tasks: LapDoc Expert System Rigor Upgrade

## Task 1: Academic Evaluation & Viva Defense Document

**Description:** Author a comprehensive academic defense document at `docs/EXPERT_SYSTEM_EVALUATION.md` analyzing LapDoc against formal AI Expert System literature (Shortliffe's MYCIN, Jackson, Russell & Norvig). Address the core question "Is this an Expert System?" by contrasting symbolic expert systems vs. machine learning/LLMs, detailing knowledge base vs. inference engine separation, working memory, explanation facilities, handling inexact/conditional knowledge ("may or may not" vs. deterministic), and boundary awareness ("knowing its limitations"). Include viva defense Q&A.

**Acceptance criteria:**
- [x] Complete breakdown of the 5 canonical components of an Expert System mapped directly to LapDoc.
- [x] Explicit contrast between Decision Tree flowcharts vs. Expert System reasoning with certainty factors.
- [x] Detailed analysis of how LapDoc handles limitations (domain boundaries, inconclusive outcomes).
- [x] Model viva/review Q&A answering common professor/evaluator critique questions.

**Verification:**
- [x] File exists at `docs/EXPERT_SYSTEM_EVALUATION.md` and contains all required sections.
- [x] Document links to codebase files and provides clear academic citations.

**Dependencies:** None

**Files likely touched:**
- `docs/EXPERT_SYSTEM_EVALUATION.md`

**Estimated scope:** Small (1 file)

---

## Task 2: Knowledge Base Enrichment with Certainty Factors & Boundary Rules

**Description:** Upgrade `knowledge_base.json` to equip diagnostic leaves with formal `certainty_factor` values ($0.0$ to $1.0$), `is_deterministic` indicators, and `competing_hypotheses` for ambiguous symptoms (e.g. black screen, sudden shutdown, thermal throttle). Add domain boundary metadata defining out-of-scope diagnostics. Update `tests/test_knowledge_base.py` to validate new schema properties.

**Acceptance criteria:**
- [x] All leaf diagnoses in `knowledge_base.json` have valid `certainty_factor` floats ($0.0 \le CF \le 1.0$) and `is_deterministic` booleans.
- [x] Ambiguous multi-cause symptom nodes include structured `competing_hypotheses` arrays.
- [x] Schema validation tests in `tests/test_knowledge_base.py` verify presence and valid ranges for the new properties.

**Verification:**
- [x] Tests pass: `.venv/bin/pytest tests/test_knowledge_base.py`
- [x] All 52 nodes pass JSON validity and schema checks.

**Dependencies:** None

**Files likely touched:**
- `knowledge_base.json`
- `tests/test_knowledge_base.py`

**Estimated scope:** Small (2 files)

---

## Task 3: Inference Engine Uncertainty & Limitation Logic

**Description:** Upgrade `engine.py` to support inexact reasoning and boundary awareness. Update `DiagnosticResult` with `confidence_score: float`, `is_deterministic: bool`, `is_inconclusive: bool`, `competing_hypotheses: List[Dict]`, and `limitation_notes: Optional[str]`. Implement MYCIN-style certainty combination functions, inconclusive threshold checks ($CF < 0.60$), and out-of-scope boundary detection. Create dedicated test suites in `tests/test_uncertainty.py` and `tests/test_boundary.py`. Ensure 100% backward compatibility with all existing engine and audit tests.

**Acceptance criteria:**
- [ ] `DiagnosticResult` includes new confidence and limitation fields with safe defaults preserving backward compatibility.
- [ ] Inexact reasoning correctly computes cumulative CF for multi-step paths.
- [ ] Diagnoses with $CF < 0.60$ or out-of-domain symptoms flag `is_inconclusive=True` with explicit limitation notes.
- [ ] 100% pass on all existing 17 tests + new tests in `test_uncertainty.py` and `test_boundary.py`.

**Verification:**
- [ ] Tests pass: `.venv/bin/pytest tests/test_uncertainty.py tests/test_boundary.py tests/test_engine.py tests/test_tree_audit.py`
- [ ] Existing callers receive expected `DiagnosticResult` objects without breaking.

**Dependencies:** Task 2

**Files likely touched:**
- `engine.py`
- `tests/test_uncertainty.py`
- `tests/test_boundary.py`
- `tests/test_engine.py`

**Estimated scope:** Medium (4 files)

---

## Checkpoint: Foundation (After Tasks 1-3)
- [ ] All unit and regression tests pass cleanly: `.venv/bin/pytest`
- [ ] Engine successfully derives both deterministic and conditional diagnoses with certainty scores.
- [ ] Domain limitations and inconclusive states are correctly detected and flagged.

---

## Task 4: CLI Terminal Integration for Confidence, Hypotheses, & Limitations

**Description:** Update `cli.py` to display certainty ratings and domain limitations in the terminal runner. In both emergency triage and audit modes, display the confidence score (e.g., `95% Confidence [DETERMINISTIC]` vs. `75% Confidence [CONDITIONAL]`), list alternative competing hypotheses when present, and print warning banners when a diagnosis hits domain limitations or is inconclusive.

**Acceptance criteria:**
- [ ] Terminal summary outputs the confidence percentage and diagnostic nature (Deterministic vs Conditional).
- [ ] When competing hypotheses exist, CLI prints a ranked list of alternative possibilities.
- [ ] When `is_inconclusive=True` or a boundary is reached, CLI prints a limitation notice advising bench diagnostics.
- [ ] CLI test suite in `tests/test_cli.py` is updated and passing.

**Verification:**
- [ ] Tests pass: `.venv/bin/pytest tests/test_cli.py`
- [ ] Manual check: `.venv/bin/python cli.py --emergency` shows confidence and hypothesis output.

**Dependencies:** Task 3

**Files likely touched:**
- `cli.py`
- `tests/test_cli.py`

**Estimated scope:** Small (2 files)

---

## Task 5: Streamlit Web UI Integration for Confidence Meters & Differential Diagnoses

**Description:** Update `app.py` to visually represent certainty and limitation boundaries. Add a visual confidence progress meter (`st.progress` / badge), color-coded pill tags (`🟢 Deterministic Physical Finding` vs. `🟡 Conditional Diagnostic Hypothesis`), a collapsible expander for `Differential Diagnostic Hypotheses`, and an alert card for `⚠️ Diagnostic Limitation / Inconclusive Finding` when confidence is below threshold or out-of-scope.

**Acceptance criteria:**
- [ ] Result views in Streamlit prominently display confidence score and deterministic vs conditional badges.
- [ ] Competing hypotheses render inside a clean, sorted UI expander.
- [ ] Inconclusive / limitation states display actionable lab advice instead of ambiguous generic verdicts.
- [ ] Web UI tests in `tests/test_app.py` pass cleanly.

**Verification:**
- [ ] Tests pass: `.venv/bin/pytest tests/test_app.py`
- [ ] Manual check: Streamlit compiles and renders without errors.

**Dependencies:** Task 3

**Files likely touched:**
- `app.py`
- `tests/test_app.py`

**Estimated scope:** Small (2 files)

---

## Checkpoint: Final Acceptance (After Tasks 4-5)
- [ ] All tests pass: `.venv/bin/pytest`
- [ ] CLI runs smoothly in all modes (`python cli.py --audit-quick`, `python cli.py --emergency`).
- [ ] Streamlit web UI renders confidence meters, differential diagnoses, and limitation notices.
