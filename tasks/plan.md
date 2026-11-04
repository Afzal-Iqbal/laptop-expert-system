# Implementation Plan: "Laptop Doctor" Clinical Diagnostic Experience

## Overview
Transform LapDoc into an empathetic, highly effective **"Laptop Doctor" clinical consultation system**. Following the confirmed statement of intent in `docs/intent/laptop_doctor_experience.md`, the system mimics a seasoned hardware physician:
- Common, well-understood hardware ailments are diagnosed immediately with 100% surety and an actionable fix ("the medicine").
- Complex or ambiguous ailments trigger the doctor to prescribe specific, non-invasive physical desk tests (e.g. flashlight test, external monitor check, power drain) and interpret test findings before drilling into targeted follow-ups.
- Diagnostic outcomes are delivered as an authoritative **Clinical Consultation Report & Prescription** (Doctor's Diagnosis, Prognosis, Prescription & Treatment Plan, and Clinical Tests Performed).

---

## Architecture Decisions

1. **Clinical Test Protocol in Knowledge Base (`knowledge_base.json`)**:
   - Equip diagnostic nodes with a structured `clinical_test` dictionary where applicable (`test_name`, `instructions`, `expected_observations`).
   - Tag nodes with `is_common` flags for immediate primary resolution, and provide structured `prescription` steps.

2. **Doctor Consultation Engine Extensions (`engine.py`)**:
   - Add clinical properties to `DiagnosticResult`: `prognosis: str`, `prescription: List[str]`, `clinical_tests_performed: List[Dict[str, str]]`.
   - Add engine methods to retrieve active diagnostic tests and generate a structured `DoctorConsultationReport`.
   - Maintain 100% backward compatibility with all existing engine APIs and data structures.

3. **Streamlit "Doctor Consultation Room" UI (`app.py`)**:
   - Rebrand the UI to the "Laptop Doctor" clinical workflow.
   - For ambiguous nodes: render a prominent **"🩺 Prescribed Diagnostic Test"** card containing step-by-step instructions on what test to run at the desk before selecting the observed symptom.
   - For diagnoses: present a doctor's **Prescription Pad & Treatment Plan** with clear DIY vs. Specialist guidance.
   - Frame the full 50-point audit as a **"Comprehensive Annual Physical / Subsystem Health Checkup"**.

4. **Terminal CLI Runner (`cli.py`)**:
   - Align terminal outputs with clinical doctor consultation styling (Prescribed Tests, Doctor Diagnosis, Prescription).

---

## Dependency Graph

```text
knowledge_base.json (Add clinical_test, is_common, and prescription tags)
       │
       ├── tests/test_knowledge_base.py (Validate schema additions)
       │
    engine.py (Add clinical test detection, DoctorConsultationReport, prognosis)
       │
       ├── tests/test_doctor_consultation.py (New test suite for doctor workflow)
       │
   ┌───┴────────────────┐
   ▼                    ▼
 app.py (Streamlit)   cli.py (Terminal)
   │                    │
   └── tests/test_app.py└── tests/test_cli.py
```

---

## Task List

### Phase 1: Knowledge Base & Engine Doctor Protocols

- [ ] **Task 1: Enrich Knowledge Base with Clinical Tests & Prescriptions**
  - Update `knowledge_base.json` to enrich nodes with `clinical_test` definitions (flashlight screen test, external monitor test, battery rail test, RAM slot swap, etc.) and `is_common` flags.
  - Update schema tests in `tests/test_knowledge_base.py`.

- [ ] **Task 2: Inference Engine Clinical Consultation Protocols & Doctor Report**
  - Enhance `DiagnosticResult` in `engine.py` with `prognosis`, `prescription`, and `clinical_tests_performed`.
  - Add helper methods to format and extract prescribed tests and generate structured doctor reports.
  - Create `tests/test_doctor_consultation.py` to test doctor consultation flow, common issue 100% surety, and ambiguous test prescribing.

### Checkpoint: Foundation
- [ ] All tests pass: `.venv/bin/pytest tests/test_knowledge_base.py tests/test_doctor_consultation.py tests/test_engine.py`
- [ ] Prescribed desk tests and common ailments correctly populate in engine results.

---

### Phase 2: User Interfaces (Web Consultation Room & Terminal Runner)

- [ ] **Task 3: Streamlit "Laptop Doctor" Consultation Room & Diagnostic Test Prompts**
  - Update `app.py` to present the consultation room experience.
  - Render active "🩺 Prescribed Diagnostic Test" instruction boxes when physical checks are needed.
  - Render the final diagnosis as a Doctor's Prescription & Treatment Plan with clear medicine/remediation steps.
  - Reframe the 50-point audit as a "Preventive Annual Physical / Health Checkup".
  - Update `tests/test_app.py`.

- [ ] **Task 4: CLI Terminal "Laptop Physician" Consultation Flow**
  - Update `cli.py` to format consultation prompts, prescribed tests, doctor diagnoses, and prescriptions in the terminal.
  - Update `tests/test_cli.py`.

### Checkpoint: Interfaces
- [ ] All tests pass: `.venv/bin/pytest tests/test_app.py tests/test_cli.py`
- [ ] Manual check: Streamlit and CLI display doctor consultation, test instructions, and prescriptions cleanly.

---

### Phase 3: Documentation & System Polish

- [ ] **Task 5: End-to-End System Validation, Regression Suite & Documentation**
  - Update `README.md` to reflect the Laptop Doctor consultation paradigm.
  - Run full test suite across all 34+ tests ensuring 100% pass rate.

### Checkpoint: Complete
- [ ] Full test suite green (`.venv/bin/pytest`).
- [ ] Both web and CLI interfaces deliver consistent, rapid, and accurate doctor-like advice to non-expert users.

---

## Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Ambiguous tests confuse non-expert users | Medium | Keep test instructions extremely simple, 2-3 steps max, using household tools (e.g., phone flashlight, HDMI cord). |
| Existing automated tests break due to schema changes | High | Keep all additions optional and backward-compatible with default fallbacks in `engine.py`. |
| Diagnostic tests require invasive teardown | High | Strictly constrain all prescribed tests to non-invasive external checks (no screwdriver/soldering required). |

---

## Open Questions
- None. Requirements and bounds confirmed during the `interview-me` session.
