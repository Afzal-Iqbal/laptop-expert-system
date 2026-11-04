# Confirmed Intent: "Laptop Doctor" Clinical Diagnostic Experience

## Background & Rationale
The user explicitly clarified the core identity and mental model of LapDoc:
Rather than presenting the system with dry, retro 1970s academic AI jargon (IF-THEN rule formalisms, CLIPS notation, inference engine theory), LapDoc must operate as an **authoritative, empathetic "Laptop Doctor"** providing clinical diagnostic consultations to everyday non-expert users.

## Core Workflow: The Doctor Consultation Model
1. **Chief Complaint & Initial Triage**:
   - The user describes their laptop's acute symptom.
2. **Immediate Diagnosis & Prescription for Common Ailments**:
   - For straightforward, well-known issues (e.g. dead charger, stuck key, dead CMOS battery), diagnose immediately with 100% certainty and provide the direct, actionable remedy ("medicine").
3. **Prescribing Safe Diagnostic Tests for Ambiguous / Complex Issues**:
   - When a problem is severe, non-obvious, or ambiguous, the doctor orders a specific, safe physical desk test (e.g. flashlight test for backlight, external monitor test for GPU/display, hard reboot with battery drain for power rail latch-up).
4. **Interpreting Test Results & Targeted Follow-Up**:
   - The system interprets the user's test findings and asks focused, problem-specific follow-up questions to pinpoint the exact failure domain.
5. **Doctor's Prescription, Prognosis & Actionable Treatment Plan**:
   - Formulate conclusions as a Doctor's Diagnosis, Treatment Plan, and Prognosis (Home DIY Remedy vs. Authorized Service Center referral), complete with estimated cost and urgency.

## Confirmed Bounds
- Non-invasive testing only (safe at the user's desk).
- Pure symbolic inference backed by the 52-scenario knowledge base.
- Clean, reassuring clinical doctor-patient persona without academic clutter.
