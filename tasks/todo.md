# Tasks: "Laptop Doctor" Clinical Diagnostic Experience

## Task 1: Enrich Knowledge Base with Clinical Tests & Prescriptions

**Description:** Upgrade `knowledge_base.json` to equip diagnostic nodes with safe, non-invasive `clinical_test` definitions (e.g. Flashlight Inversion Test for dark screens, External Monitor Bypass for GPU verification, Power Rail Flea-Drain for unbootable states, Vent Thermal Feel Check for fans). Add `is_common` boolean indicators to common hardware ailments and link actionable, direct remedies (`prescription`). Update `tests/test_knowledge_base.py` to validate new schema properties.

**Acceptance criteria:**
- [x] Nodes requiring physical disambiguation in `knowledge_base.json` contain structured `clinical_test` objects (`test_name`, `instructions`, `expected_observations`).
- [x] Obvious/common diagnostic leaves are flagged with `is_common=True` and contain 100% certainty factor.
- [x] Schema validation tests in `tests/test_knowledge_base.py` verify that `clinical_test` objects follow the expected structure without regressions.

**Verification:**
- [x] Tests pass: `.venv/bin/pytest tests/test_knowledge_base.py`
- [x] Schema passes JSON parsing and all 52 nodes validate cleanly.

**Dependencies:** None

**Files likely touched:**
- `knowledge_base.json`
- `tests/test_knowledge_base.py`

**Estimated scope:** Small (2 files)

---

## Task 2: Inference Engine Clinical Consultation Protocols & Doctor Report

**Description:** Update `engine.py` to support the "Laptop Doctor" consultation flow. Add `prognosis: str`, `prescription: List[str]`, and `clinical_tests_performed: List[Dict[str, str]]` to `DiagnosticResult` while ensuring 100% backward compatibility. Add helper methods to detect when a node prescribes a clinical test and generate a structured `DoctorConsultationReport`. Create a new test suite in `tests/test_doctor_consultation.py` validating common-issue immediate resolution and complex test prescribing.

**Acceptance criteria:**
- [x] `DiagnosticResult` includes `prognosis`, `prescription`, and `clinical_tests_performed` with safe defaults.
- [x] Common issues resolve with 100% certainty and direct prescription ("medicine").
- [x] Ambiguous symptom nodes expose prescribed clinical desk tests that are captured in the consultation history trace.
- [x] New test file `tests/test_doctor_consultation.py` passes all unit tests for the doctor workflow.

**Verification:**
- [x] Tests pass: `.venv/bin/pytest tests/test_doctor_consultation.py tests/test_engine.py`

**Dependencies:** Task 1

**Files likely touched:**
- `engine.py`
- `tests/test_doctor_consultation.py`
- `tests/test_engine.py`

**Estimated scope:** Medium (3 files)

---

## Checkpoint: Foundation (After Tasks 1-2)
- [x] All tests pass: `.venv/bin/pytest tests/test_knowledge_base.py tests/test_doctor_consultation.py tests/test_engine.py`
- [x] Engine successfully models common 100% certainty triage vs. clinical desk test prescriptions for complex cases.

---

## Task 3: Streamlit "Laptop Doctor" Consultation Room & Diagnostic Test Prompts

**Description:** Overhaul `app.py` to create the "Laptop Doctor" clinical consultation experience. When an ambiguous node is reached, render a dedicated, prominent **"🩺 Doctor's Order: Prescribed Diagnostic Test"** card detailing the safe physical test instructions. For final diagnoses, render an authentic **Doctor's Prescription & Discharge Plan** (Chief Complaint, Doctor's Diagnosis, Prognosis, Prescription Medicine, and Tests Performed). Reframe the 50-point audit as a "Preventive Annual Physical / Health Checkup". Update `tests/test_app.py`.

**Acceptance criteria:**
- [x] Triage flow displays doctor persona with clear patient intake context.
- [x] Nodes with physical tests render a distinct "🩺 Prescribed Diagnostic Test" guidance box with step-by-step instructions.
- [x] Final result presents an actionable Doctor's Prescription card with clear Home Remedy vs. Specialist Referral tags.
- [x] Web UI tests in `tests/test_app.py` pass without error.

**Verification:**
- [x] Tests pass: `.venv/bin/pytest tests/test_app.py`
- [x] Manual check: Streamlit compiles and displays the Doctor Consultation interface cleanly.

**Dependencies:** Task 2

**Files likely touched:**
- `app.py`
- `tests/test_app.py`

**Estimated scope:** Medium (2 files)

---

## Task 4: CLI Terminal "Laptop Physician" Consultation Flow

**Description:** Update `cli.py` to format terminal triage as a clinical doctor consultation. Display consultation steps, format prescribed physical desk tests prominently (`[🩺 Doctor's Prescribed Test]`), and print the final output as a Doctor's Diagnosis & Prescription. Ensure all existing CLI flags (`--emergency`, `--audit`, `--audit-quick`) continue to work seamlessly. Update `tests/test_cli.py`.

**Acceptance criteria:**
- [x] Terminal runner introduces the session as a Doctor's Diagnostic Consultation.
- [x] Prescribed desk tests are highlighted with step-by-step instructions before asking for the observed outcome.
- [x] Diagnosis output is formatted as Doctor's Diagnosis, Prognosis, and Prescription.
- [x] CLI test suite in `tests/test_cli.py` passes cleanly.

**Verification:**
- [x] Tests pass: `.venv/bin/pytest tests/test_cli.py`
- [x] Manual check: `python cli.py --emergency` displays doctor consultation prompts.

**Dependencies:** Task 2

**Files likely touched:**
- `cli.py`
- `tests/test_cli.py`

**Estimated scope:** Small (2 files)

---

## Checkpoint: Interfaces (After Tasks 3-4)
- [x] All tests pass: `.venv/bin/pytest tests/test_app.py tests/test_cli.py`
- [x] Web and CLI interfaces both deliver the clinical doctor consultation experience.

---

## Task 5: End-to-End System Validation, Regression Suite & Documentation

**Description:** Update `README.md` to explain the Laptop Doctor consultation paradigm (Common Ailments 100% Surety, Desk Test Prescriptions for Ambiguity, Doctor's Prescription & Treatment Plan). Run the entire test suite across all test files to verify zero regressions.

**Acceptance criteria:**
- [x] `README.md` accurately documents the Laptop Doctor workflow and consultation features.
- [x] 100% test pass rate across all test files in `tests/`.

**Verification:**
- [x] Tests pass: `.venv/bin/pytest`

**Dependencies:** Tasks 3 & 4

**Files likely touched:**
- `README.md`

**Estimated scope:** Small (1 file)

---

## Checkpoint: Complete (After Task 5)
- [x] Full test suite green (`.venv/bin/pytest`).
- [x] Complete system verified in both Web and CLI modes.

