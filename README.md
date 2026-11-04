# LapDoc: The Laptop Physician & Hardware Diagnostic Expert System

**LapDoc** is a classical Artificial Intelligence Expert System designed to mimic the clinical decision-making abilities of a seasoned hardware physician. It diagnoses complex laptop hardware, firmware, and operating system issues through a declarative knowledge base of **52 structured diagnostic protocols**, safe physical desk tests, and forward-chaining inference rules.

---

## The "Laptop Doctor" Consultation Paradigm

LapDoc operates on an intuitive doctor consultation model tailored for everyday, non-expert users:

1. **Chief Complaint & Immediate 100% Surety for Common Ailments**:
   - For straightforward, high-frequency hardware ailments (e.g. dead AC adapter, swollen lithium-ion battery, CMOS cell depletion, stuck power button), the doctor diagnoses the issue immediately with **100% certainty** and prescribes a clear, actionable remedy ("the medicine").

2. **Prescribing Safe Diagnostic Desk Tests for Ambiguous Issues**:
   - When symptoms are complex or ambiguous, the doctor orders specific, safe, non-invasive physical desk tests (e.g., the *Smartphone Flashlight Screen Test* for dark displays, *External Video Bypass Check* for GPU isolation, *Flea Power Drain* for power-rail latch-ups, *Acoustic Stethoscope Check* for drive failures).
   - The user conducts the test at their desk and reports the finding back to the doctor.

3. **Targeted Follow-Up & Clinical Differential Diagnoses**:
   - The engine interprets the test outcome and asks focused, problem-specific follow-up questions to isolate the root cause, ranking alternative competing hypotheses when reasoning under inexact knowledge.

4. **Doctor's Prescription & Actionable Treatment Plan**:
   - Conclusions are delivered as an authoritative **Doctor's Consultation Report**:
     - **🩺 Doctor's Diagnosis**: Pathology mechanism and certainty score.
     - **📋 Clinical Prognosis**: Safe Home DIY Remedy vs. Certified Board Technician Referral.
     - **💊 Actionable Prescription Pad**: Step-by-step numbered doctor's orders (`Rx 1`, `Rx 2`).
     - **🔬 Clinical Tests Conducted**: Record of desk tests verified during the consultation.

5. **Comprehensive Annual Physical (50-Point Subsystem Audit)**:
   - In addition to emergency triage, LapDoc offers a full systematic health checkup across all 7 hardware domains, evaluating 52 checkpoints with letter grades and estimated repair expense scorecards.

---

## System Architecture

```
┌────────────────────────────────────────────────────────┐
│                   LAPDOC EXPERT SYSTEM                 │
│                                                        │
│  ┌────────────────────────┐    ┌────────────────────┐  │
│  │     KNOWLEDGE BASE     │    │   WORKING MEMORY   │  │
│  │ (Declarative Protocols,│    │ (Patient Intake,   │  │
│  │  Clinical Tests, CFs)  │    │  Reported Findings)│  │
│  └───────────┬────────────┘    └─────────┬──────────┘  │
│              │                           │             │
│              ▼                           ▼             │
│  ┌──────────────────────────────────────────────────┐  │
│  │                INFERENCE ENGINE                  │  │
│  │   • Forward Graph-Traversal Inference            │  │
│  │   • Clinical Desk Test Evaluation & Pruning      │  │
│  │   • MYCIN Certainty Factor ($CF$) Propagation    │  │
│  └───────────────────────┬──────────────────────────┘  │
│                          │                             │
│                          ▼                             │
│  ┌──────────────────────────────────────────────────┐  │
│  │              EXPLANATION FACILITY                │  │
│  │   • "WHY": Doctor's Clinical Objective           │  │
│  │   • "HOW": Evidentiary Deduction Trace           │  │
│  └───────────────────────┬──────────────────────────┘  │
│                          │                             │
│                          ▼                             │
│  ┌──────────────────────────────────────────────────┐  │
│  │                 USER INTERFACE                   │  │
│  │   • Streamlit Consultation Room (app.py)         │  │
│  │   • Terminal Physician Runner (cli.py)           │  │
│  └──────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────┘
```

- **Declarative Knowledge Base (`knowledge_base.json`)**: Zero hardware logic is hardcoded in application code. All 52 nodes, clinical desk test instructions, gateway checks, and certainty factors are stored declaratively.
- **Inference Engine (`engine.py`)**: Domain-independent forward-chaining engine supporting early-exit triage, cascading tree audits, certainty propagation, and doctor report generation.
- **Web Consultation Room (`app.py`)**: Responsive Streamlit interface featuring prescribed test instruction cards, doctor's prescription pads, and interactive audit scorecards.
- **Terminal Runner (`cli.py`)**: Complete command-line physician consultation suite.

---

## Quickstart

### 1. Setup Virtual Environment
```bash
# Clone or navigate to directory
cd /home/afzal/Projects/laptop-expert-system

# Activate virtualenv
source .venv/bin/activate
```

### 2. Run the Streamlit Web Application
```bash
streamlit run app.py
```
Open `http://localhost:8501` in your browser.

### 3. Run the CLI Terminal Runner
```bash
# Interactive Physician Menu
python cli.py

# Direct Urgent Consultation (Emergency Fast-Triage)
python cli.py --emergency

# Direct 50-Point Annual Physical (Comprehensive Audit)
python cli.py --audit

# Quick Smoke Checkup (Auto-fills healthy defaults)
python cli.py --audit-quick
```

### 4. Run Automated Test Suite
```bash
pytest
```

---

## Monitored Hardware Domains (7 Subsystems)

| Subsystem Domain | Checkpoints | Clinical Diagnostic Coverage |
| :--- | :---: | :--- |
| **Power & Battery** | 8 | AC adapter, DC jack, PMIC short circuit, battery swelling, flea-power drain, SMBus lockout |
| **Display & Graphics** | 8 | Backlight fuse, flashlight test, eDP cable hinge pinch, external video bypass, dead pixels |
| **Thermals & Cooling** | 6 | Bearing grinding, thermal paste pump-out, heatsink fin clog, exhaust airflow check |
| **Storage & Boot** | 7 | S.M.A.R.T. health, drive acoustic stethoscope, bootloader corruption, BSOD stop codes |
| **Memory & Performance** | 6 | RAM channel training, POST beep & blink diagnostic codes, memory bit-flips |
| **Peripherals & I/O** | 9 | Keyboard matrix test, trackpad dome switches, USB ports, Hall-effect lid sensor test |
| **Connectivity & Audio** | 8 | Wi-Fi antenna detachment, Bluetooth host, speaker diaphragm, chassis hinge integrity |

---

## Academic Evaluation & Literature Reference
A formal academic defense evaluating LapDoc against classical AI Expert System literature (Shortliffe's MYCIN, Jackson's *Introduction to Expert Systems*, Russell & Norvig's *AIMA*) is available in [`docs/EXPERT_SYSTEM_EVALUATION.md`](docs/EXPERT_SYSTEM_EVALUATION.md).
