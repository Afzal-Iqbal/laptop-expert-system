# Tasks: Streamline App & Remove Unnecessary Bloat

## Task 1: Clean Dead Code, Unused Widgets, and Orphaned CSS from `app.py`

**Description:** Remove dead code and unused assets from `app.py`. Eliminate the unused `chassis_type` (Form Factor / Chassis) selectbox widget from the sidebar, remove the dead assignment `report = engine.generate_doctor_report(...)` on line 190, purge orphaned CSS rules (`.doctor-card`, `.prescription-box`, `.test-box`), and replace the remote CDN image with native emoji rendering.

**Acceptance criteria:**
- [x] `chassis_type` selectbox is removed from the sidebar.
- [x] Dead variable assignment `report = engine.generate_doctor_report(...)` is eliminated.
- [x] Unused CSS classes `.doctor-card`, `.prescription-box`, and `.test-box` are removed.
- [x] Remote `icons8.com` image URL is replaced with local/native icon rendering (`🩺`).

**Verification:**
- [x] Syntax check: `.venv/bin/python -m py_compile app.py`
- [x] Tests pass: `.venv/bin/pytest tests/test_app.py`

**Dependencies:** None

**Files likely touched:**
- `app.py`

**Estimated scope:** Small (1 file)

---

## Task 2: Streamline Consultation Modes in `app.py` (Remove Academic Rubric Proof)

**Description:** Remove the 3rd mode ("📚 Knowledge Base & 52 Conditions (Rubric Proof)") from `app.py`. Consolidate the consultation service radio selector in the sidebar to only the 2 real user-facing diagnostic workflows (`⚡ Emergency Fast-Triage` and `🔍 Cascading Decision-Tree Audit`). Remove the academic rubric checklist and 52-condition explorer dataframe from lines 519-587.

**Acceptance criteria:**
- [x] `app_mode` radio options contain only `⚡ Emergency Fast-Triage` and `🔍 Cascading Decision-Tree Audit`.
- [x] The academic rubric table, KPI cards, and condition explorer block (lines 519-587) are removed from `app.py`.
- [x] Triage flow, 50-point audit flow, and mode switching between them remain 100% functional.

**Verification:**
- [x] Tests pass: `.venv/bin/pytest tests/test_app.py`

**Dependencies:** Task 1

**Files likely touched:**
- `app.py`

**Estimated scope:** Small (1 file)

---

## Checkpoint: Streamlit UI Clean & Passing (After Tasks 1-2)
- [x] `app.py` compiles cleanly without errors: `.venv/bin/python -m py_compile app.py`
- [x] All UI tests in `tests/test_app.py` pass cleanly.

---

## Task 3: Clean Repository Root Duplicate Files and Update `.gitignore`

**Description:** Safely remove the two duplicate PDF report files from the repository root (`CT_24263_Muhammad Afzal Iqbal_Lab_011_OOAD.pdf` and `Muhammad_Afzal_Iqbal_CT_24263_A_Expert_System_CCP.pdf`), verifying that canonical copies remain safely preserved in `docs/`. Update `.gitignore` to ignore the `scratch/` directory and root-level PDFs.

**Acceptance criteria:**
- [x] Canonical copies of both PDFs exist and are preserved in `docs/`.
- [x] Redundant 2.2MB duplicate PDFs in the repository root are removed.
- [x] `.gitignore` contains rules for `scratch/` and root `*.pdf`.

**Verification:**
- [x] Git status: `git status` shows clean tracking with no untracked duplicate PDFs or scratch folder.
- [x] File check: `ls docs/*.pdf` confirms canonical documents are intact.

**Dependencies:** None

**Files likely touched:**
- `.gitignore`
- `CT_24263_Muhammad Afzal Iqbal_Lab_011_OOAD.pdf` (deleted)
- `Muhammad_Afzal_Iqbal_CT_24263_A_Expert_System_CCP.pdf` (deleted)

**Estimated scope:** Small (1 file modified, 2 root duplicates removed)

---

## Task 4: Full Regression and Verification Suite

**Description:** Execute the entire automated test suite and runtime compilation check across the whole project to guarantee 100% backward compatibility, verify that all 8 test modules pass cleanly, and confirm that both the Web UI and CLI runners remain completely functional.

**Acceptance criteria:**
- [x] All 42 automated tests pass across all test modules in `tests/`.
- [x] CLI runner `--emergency` and `--audit` flags remain functional.
- [x] Streamlit `app.py` compiles and initializes without runtime errors.

**Verification:**
- [x] Tests pass: `.venv/bin/pytest`
- [x] CLI syntax: `.venv/bin/python cli.py --help`

**Dependencies:** Tasks 1, 2, and 3

**Files likely touched:**
- None (verification only)

**Estimated scope:** XS (0 files modified)

---

## Task 5: Update Documentation & Final Polish

**Description:** Update `README.md` to reflect the streamlined application (clean 2-mode consultation experience, offline-native assets, and minimal configuration). Perform final regression run to ensure complete project health.

**Acceptance criteria:**
- [x] `README.md` documents the clean 2-mode diagnostic workflow and offline capability.
- [x] Full test suite passes: `.venv/bin/pytest`.

**Verification:**
- [x] Tests pass: `.venv/bin/pytest`
- [x] Documentation view: `README.md` reflects current application state.

**Dependencies:** Tasks 1, 2, 3, 4

**Files likely touched:**
- `README.md`

**Estimated scope:** Small (1 file)

---

## Checkpoint: Complete System Verification & Polish (After Task 5)
- [x] 100% of tests green in `.venv/bin/pytest`.
- [x] App and documentation are streamlined, lean, and free of unnecessary code and assets.
