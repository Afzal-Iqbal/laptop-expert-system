# Dual-Mode Laptop Diagnostic Expert System (`LapDoc`)

## Problem Statement
How might we build an intelligent, rule-driven laptop troubleshooting system in Python and Streamlit that provides instantaneous root-cause diagnosis for urgent failures, while also offering an exhaustive 50-point hardware audit for pre-purchase inspections?

## Recommended Direction
Build a **Unified Knowledge Graph with Dual Traversal Engine** wrapped in a clean Streamlit interface.

The entire knowledge base of 50+ questions, symptom triggers, and remediation procedures lives in a structured declarative format (`knowledge_base.json`). A Python `InferenceEngine` class handles two traversal algorithms:
1. **Emergency Fast-Triage:** Dynamic DAG traversal with priority heuristics and early-exit leaf resolution (4–8 questions).
2. **50-Point Pre-Purchase / Routine Audit:** Sequential category evaluation generating a composite **Health Scorecard (0–100%)**, an estimated repair bill, and a downloadable diagnostic summary.

Includes an **Explanation Facility** so users can inspect *"Why is this question asked?"* or view the final rule execution path (*"How this conclusion was derived"*).

## Key Assumptions to Validate
- [ ] **Symptom Disambiguation:** 50 diagnostic rules can accurately differentiate between common confusing overlaps (e.g., Bad RAM vs. Corrupted OS vs. Failing SSD boot failure).
- [ ] **Streamlit State Resilience:** Dynamic DAG navigation handles user backtracking or revising prior answers without crashing `st.session_state`.
- [ ] **Audit Completion Viability:** Grouping the 50 checks into 6 discrete visual subsystems makes the complete audit feel quick (< 4 minutes) rather than exhausting.

## MVP Scope
- **Declarative Knowledge Base (`knowledge_base.json`):** 50+ structured questions across 6 subsystems (Power, Display, Thermals, Storage/Boot, Memory, Peripherals/Audio).
- **Inference Engine (`engine.py`):** Fast DAG traversal with early leaf exit and comprehensive audit scoring.
- **Explanation Facility:** Exposing the reasoning path.
- **Streamlit Web UI (`app.py`):** Interactive UI for both modes.
- **Automated Test Suite (`tests/`):** Graph cycle checks, schema validation, and score calculation verification.

## Not Doing (and Why)
- OS-level automated scraping (`psutil`): Keeps the system pure, platform-independent, and focused on expert reasoning.
- Generic LLM wrappers: Uses deterministic expert rules to guarantee explainability and academic rigor.
