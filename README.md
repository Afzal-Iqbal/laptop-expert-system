# LapDoc: Laptop Diagnostic Expert System

**LapDoc** is a classical Artificial Intelligence Expert System built with Python and Streamlit. It diagnoses complex laptop hardware, firmware, and operating system issues through a declarative knowledge base of **52 structured diagnostic questions** and rules.

---

## Key Features

1. **Dual Operating Modes**:
   - **⚡ Emergency Fast-Triage**: A Directed Acyclic Graph (DAG) with greedy conditional pruning and **early-exit resolution**. Diagnoses acute issues (blown backlight fuse, short circuits, dead RAM, thermal runaway) in just **2 to 8 questions**.
   - **🔍 50-Point Subsystem Audit**: An exhaustive inspection across 7 hardware domains (Power & Battery, Display & GPU, Thermals & Cooling, Storage & Boot, RAM & Performance, Peripherals & I/O, Audio & Connectivity) providing a comprehensive **Health Score (0-100%)**, a **Condition Grade (A+ to F)**, and estimated repair expenses.

2. **MYCIN-Style Explanation Facility**:
   - **"Why is the system asking this?"**: Transparently reveals what fault hypothesis is being tested or eliminated at every step.
   - **"How was this conclusion derived?"**: Generates the complete inference trace from root symptoms to final diagnosis.

3. **Separation of Concerns**:
   - Core knowledge base in declarative `knowledge_base.json`.
   - Reusable inference engine in `engine.py`.
   - Standalone terminal runner in `cli.py`.
   - Modern responsive Web UI in `app.py` (Streamlit).

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
# Interactive Menu
python cli.py

# Or directly in Emergency Fast-Triage mode
python cli.py --emergency

# Or directly in 50-Point Audit mode
python cli.py --audit

# Or run quick smoke audit (auto-fills healthy checks)
python cli.py --audit-quick
```

### 4. Run Automated Test Suite
```bash
pytest
```

---

## Monitored Subsystems

| Subsystem | Questions | Diagnostic Coverage |
| :--- | :---: | :--- |
| **Power & Battery** | 8 | AC adapter, DC jack, PMIC short circuit, battery swelling, SMBus lockout |
| **Display & Graphics** | 8 | Backlight fuse, eDP cable pinch, VRAM artifacts, dead pixels, MUX switch |
| **Thermals & Cooling** | 6 | Bearing grinding, thermal paste pump-out, heatsink fin clog, thermal trip |
| **Storage & Boot** | 7 | S.M.A.R.T. degradation, EFI bootloader corruption, BSOD stop codes, BitLocker |
| **Memory & Performance** | 6 | RAM channel training failure, MemTest bit-flips, POST beep codes |
| **Peripherals & I/O** | 9 | Keyboard matrix corrosion, trackpad dome switches, USB ports, webcam, Hall sensor |
| **Connectivity & Audio** | 8 | Wi-Fi antenna detachment, Bluetooth host, speaker diaphragm, hinge standoffs |
