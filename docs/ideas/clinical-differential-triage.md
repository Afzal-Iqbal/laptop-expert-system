# Idea: Clinical Differential Triage & Context-Isolated Inference (`LapDoc v3`)

## Problem Statement
How Might We eliminate irrelevant cross-subsystem question leakage (e.g. asking about Wi-Fi/Bluetooth during a system freeze) so that LapDoc behaves like a clinical diagnostic expert—asking strictly relevant questions to isolate the chief complaint before offering any broader hardware audit?

## Recommended Direction: Symptom-First Differential Triage with Post-Diagnosis QA Audit
Transform LapDoc's inference model from a static chained decision graph into a two-phase clinical diagnostic workflow:

1. **Phase 1: Chief Complaint & Differential Pruning (Triage)**
   - The user selects or inputs their primary issue (e.g. *Sudden Freezing*, *No Display*, *Power Cutoff*).
   - The engine establishes a **Candidate Hypothesis Set** (e.g. for Freezing: `[RAM Bit-Flips, CPU Thermal Throttling, Corrupted GPU Driver, SSD Controller Timeout]`).
   - The engine asks **only disambiguating questions directly relevant to the active hypotheses** (e.g., *"Does it freeze in BIOS or Safe Mode?"*, *"Does the mouse cursor freeze or just the active window?"*).
   - Zero questions regarding unrelated hardware (Wi-Fi, Bluetooth, Audio, Hinge integrity) are asked.
   - The triage concludes as soon as the candidate set converges to the root diagnosis or hits an inconclusive boundary.

2. **Phase 2: Post-Diagnosis Quality Assurance / Preventive Audit (Optional)**
   - Once the chief complaint is diagnosed and remediation is provided, the user is offered:
     *"Primary issue diagnosed. Would you like to conduct a 50-point Quality Assurance inspection on the remaining healthy subsystems?"*
   - If accepted, the system checks the rest of the laptop to generate the comprehensive scorecard and repair estimate.

## Key Assumptions to Validate
- [ ] **Symptom Relevance Matrix**: Every question in `knowledge_base.json` can be cleanly mapped to the specific faults it helps diagnose or rule out.
- [ ] **Universal Disambiguation Power**: A single high-yield question (e.g., *"Does the failure happen in BIOS / Safe Mode?"*) can immediately eliminate 50% of candidate faults (distinguishing hardware vs. software/OS).
- [ ] **User Experience**: Users prefer resolving their immediate acute pain point in 3–5 laser-focused questions before being asked about broader hardware health.

## MVP Scope
- **Knowledge Base Refactor (`knowledge_base.json`)**: Remove all cross-subsystem `next_question` leaks (e.g. `q_random_freezing` -> `q_keyboard_keys` -> `q_wifi_reception`).
- **Differential Filter in `engine.py`**: Questions are chosen strictly within the active symptom cluster.
- **Hardware vs. Software Disambiguation**: Add explicit isolation questions (e.g. Safe Mode test for freezes/crashes) to cleanly separate OS driver faults from physical RAM/CPU defects.
- **Unified Interface Flow (`app.py` & `cli.py`)**: Unified starting point: Acute Problem Triage $\rightarrow$ Remediation $\rightarrow$ Optional Subsystem Audit.

## Not Doing (and Why)
- **Arbitrary sequential conveyor belts**: Completely eliminating the practice of passing users from one hardware subsystem to another without their consent.
- **LLM/Black-Box NLP scraping**: Keeping rules deterministic and explainable to maintain academic expert system compliance.

## Open Questions
- When diagnosing a freeze, should the first disambiguation question always be the **"BIOS / Safe Mode test"** to separate hardware from software immediately?
