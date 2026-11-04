# Spec: LapDoc Expert System Rigor Upgrade (Certainty Factors & Boundary Awareness)

## Objective
The objective of this upgrade is two-fold:
1. **Academic Defense & Literature Grounding**: Provide a formal evaluation document (`docs/EXPERT_SYSTEM_EVALUATION.md`) comparing LapDoc against classical AI Expert System literature (e.g., Shortliffe's MYCIN, Jackson's *Introduction to Expert Systems*, and Russell & Norvig's *AIMA*), clearly defining where the project adheres to classical principles, where it diverges, and how it handles limitations.
2. **Engine & Knowledge Base Rigor Upgrade**: Enhance `engine.py` and `knowledge_base.json` to move beyond pure deterministic decision trees by introducing:
   - **Reasoning Under Inexact Knowledge (Certainty Factors)**: Support both deterministic ("hardcoded", $CF = 1.0$) and conditional/probabilistic ("may or may not", $0.0 < CF < 1.0$) diagnostic conclusions, with multi-hypothesis ranking.
   - **Explicit Boundary & Limitation Awareness ("Knowing What It Knows and Doesn't Know")**: Detect out-of-domain scenarios, contradictory symptom patterns, and low-confidence thresholds, cleanly returning an "Inconclusive / Diagnostic Limitation" state instead of arbitrary false-negative conclusions.
   - **Enhanced Explanation Facility**: Extend the "How" inference trace to show the cumulative Certainty Factor and competing hypotheses considered.

---

## Tech Stack
- **Language**: Python 3.10+ (tested on Python 3.14)
- **Frameworks/Libraries**: Streamlit (Web UI), Pytest (Automated Testing)
- **Standard Library**: `dataclasses`, `typing`, `json`, `math`, `re`, `os`
- **Zero Heavy/Black-Box Dependencies**: Pure symbolic AI without LLM or black-box neural networks, ensuring 100% deterministic explainability and academic compliance.

---

## Commands
- **Run Test Suite**: `.venv/bin/pytest`
- **Run Streamlit Web App**: `.venv/bin/streamlit run app.py`
- **Run CLI Terminal Runner**: `.venv/bin/python cli.py`
- **Run Emergency Mode in CLI**: `.venv/bin/python cli.py --emergency`
- **Run Audit Mode in CLI**: `.venv/bin/python cli.py --audit`

---

## Project Structure
```text
laptop-expert-system/
├── app.py                           # Streamlit Web UI (add CF confidence meters & limitation notices)
├── cli.py                           # Terminal CLI runner (add CF display & limitation flags)
├── engine.py                        # Core Inference Engine (add CF math, hypothesis ranking, limitation engine)
├── knowledge_base.json              # Declarative Knowledge Base (add certainty_factor, boundary_rules)
├── docs/
│   ├── EXPERT_SYSTEM_EVALUATION.md  # Formal Academic Evaluation Matrix & Viva Defense Guide
│   ├── ideas/                       # Concept notes
│   └── intent/                      # Confirmed statements of intent
├── SPEC.md                          # This specification
├── tests/
│   ├── test_engine.py               # Existing engine tests
│   ├── test_knowledge_base.py       # Knowledge base validation tests
│   ├── test_tree_audit.py           # Subsystem pipeline tests
│   ├── test_uncertainty.py          # NEW: Tests for Certainty Factor propagation & hypothesis ranking
│   └── test_boundary.py             # NEW: Tests for limitation detection & out-of-scope triggers
└── .venv/                           # Python virtual environment
```

---

## Code Style & Architectural Conventions
- **Pure Symbolic Separation**: Domain facts remain strictly declarative in `knowledge_base.json`. The inference algorithms in `engine.py` must remain domain-independent.
- **Strict Typing**: Use Python `typing` (`Dict`, `List`, `Optional`, `Tuple`, `Union`) and `@dataclass`.
- **Certainty Factor Mathematics**:
  - For positive independent evidence:
    $$CF_{combined}(A, B) = CF_A + CF_B \times (1 - CF_A)$$
  - For single-leaf rules: Rule CF scaled by symptom certainty (default 1.0 when confirmed by user selection).
  - Explicit distinction between **Deterministic Rules** ($CF = 1.0$, e.g., blown fuse with visible burn mark) and **Conditional Hypotheses** ($CF \in [0.4, 0.85]$, e.g., black screen with power LED indicating GPU vs. RAM vs. Backlight).

---

## Testing Strategy
- **Framework**: `pytest` running inside `.venv`.
- **Test Categories**:
  1. **Schema & Knowledge Base Validation** (`test_knowledge_base.py`): Ensure all nodes have valid `certainty_factor` values (between 0.0 and 1.0) and valid boundary fallback definitions.
  2. **Certainty Factor Mathematical Correctness** (`test_uncertainty.py`): Verify combinations of multiple symptoms produce correct bounded CF values.
  3. **Limitation & Inconclusive Handling** (`test_boundary.py`): Verify that contradictory symptoms or confidence below threshold ($CF < 0.60$) triggers a structured `is_inconclusive = True` with clear domain limitation explanations.
  4. **Regression Safety**: All 17 existing tests in `test_engine.py`, `test_app.py`, `test_cli.py`, `test_tree_audit.py`, and `test_knowledge_base.py` must pass unchanged.

---

## Boundaries
- **Always**:
  - Run `.venv/bin/pytest` before and after making any edits.
  - Maintain backward compatibility for existing callers of `DiagnosticResult` and `process_emergency_step`.
  - Preserve all existing 52 questions and options in `knowledge_base.json`.
- **Ask First**:
  - If changing the default certainty threshold (currently proposed at 0.60).
  - If adding new top-level subsystems to `knowledge_base.json`.
- **Never**:
  - Never import external machine learning / LLM APIs (OpenAI, Gemini, torch, sklearn) to keep the expert system purely symbolic and rule-based.
  - Never remove or break existing CLI flags (`--emergency`, `--audit`, `--audit-quick`).

---

## Success Criteria
1. **Academic Evaluation Document (`docs/EXPERT_SYSTEM_EVALUATION.md`)**:
   - Rigorously details: (1) Architecture comparison with MYCIN/DENDRAL/CLIPS, (2) Declarative Knowledge Base vs. Inference Engine separation, (3) Boundary & limitation awareness, (4) Inexact reasoning ("may or may not" / conditional vs. deterministic).
   - Serves as a ready-to-use defense/viva reference.
2. **Certainty Factor & Inexact Reasoning in Engine**:
   - `DiagnosticResult` includes `confidence_score: float` ($0\% - 100\%$), `is_deterministic: bool`, and `competing_hypotheses: List[Dict]`.
   - Leaves in `knowledge_base.json` define their intrinsic certainty factors (e.g., 0.95 for exact physical indicator, 0.70 for non-specific symptom).
3. **Domain Limitation & Out-of-Scope Detection**:
   - `engine.py` identifies when symptoms indicate out-of-scope failures (e.g., liquid corrosion requiring board-level microsoldering, unidentifiable intermittent faults) or when certainty is below threshold, outputting an explicit limitation declaration.
4. **UI & CLI Presentation**:
   - Streamlit displays confidence badges (e.g. `95% Confidence (Deterministic)` or `70% Confidence (Conditional)`) and competing possibilities.
   - CLI prints confidence percentage and limitation notices.
5. **Automated Verification**:
   - 100% pass on all existing 17 tests + all new certainty and boundary tests.

---

## Open Questions
1. **Certainty Threshold**: Is $60\%$ ($CF = 0.60$) the ideal cutoff below which LapDoc flags a diagnosis as "Inconclusive / Requires Physical Bench Diagnostics", or would you prefer a different threshold (e.g., $50\%$ or $70\%$)?
2. **Competing Hypotheses Display**: In conditional situations (e.g., Black Screen), should LapDoc show top 2 or top 3 ranked alternate possibilities alongside the primary recommendation?
