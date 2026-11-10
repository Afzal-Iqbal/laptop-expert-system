# Idea One-Pager: LapDoc WAN Deployment & 50-Condition Compliance

## Problem Statement
How might we build, prove, and deploy a Python-based Expert System in a unique, non-trivial niche with 50+ auditable conditions, accessible live on the public WAN via Streamlit, so that any evaluator or user has immediate, undeniable proof that all five rubric conditions are fully met?

---

## Rubric Compliance Blueprint (The 5 Mandatory Conditions)

| Rubric Condition | LapDoc Fulfillment Strategy | Technical Verification |
| :--- | :--- | :--- |
| **1. Python Expert System** | Pure Symbolic AI architecture in Python 3.10+ (`engine.py` + `knowledge_base.json`). Complete separation of domain knowledge from control flow. Implements MYCIN certainty factor mathematics ($CF \in [0.0, 1.0]$) and dual explanation facility ("Why" and "How"). | Zero black-box neural networks/LLMs. 100% deterministic & explainable. Complies with Russell & Norvig / Shortliffe expert system definitions. |
| **2. Minimum 50 Conditions** | Declarative knowledge base with **52 structured diagnostic condition nodes** and **41 distinct leaf outcomes** across 7 hardware subsystems. | Dedicated **"📚 Knowledge Base & 52-Condition Inspector"** tab in Streamlit displaying a live condition counter (`52/50`), antecedent-consequent rules, and automated pytest validation (`test_kb_has_above_50_questions`). |
| **3. Unique Niche** | **"Laptop Doctor" Clinical Hardware & Firmware Triage**: Instead of toy textbook problems (car repair, animal guessing), LapDoc models an empathetic hardware physician prescribing non-invasive physical desk tests (Smartphone Flashlight Test, External Video Bypass, Flea Power Capacitor Drain, Hinge Flexion Test). | Stands out immediately from standard student submissions; provides genuine real-world utility for everyday laptop owners. |
| **4. Mandatory Streamlit UI** | Interactive Web Consultation Room built 100% in Streamlit (`app.py`). Features Doctor Intake profiles, prominent "Prescribed Desk Test" instruction cards, and authentic "Prescription Pad & Treatment Plans". | Clean, responsive, WCAG-compliant UI with live subsystem pipeline steppers and exportable Markdown scorecards. |
| **5. Live WAN Accessibility** | Deploy live to the public internet via **Streamlit Community Cloud** (permanent free HTTPS URL, e.g., `lapdoc.streamlit.app`) directly connected to the project's GitHub repository. | Accessible from any browser/device globally with 24/7 uptime and automated CI/CD redeployment on git push. |

---

## Recommended Implementation Plan

### Step 1: Add Knowledge Base & 52-Condition Inspector Tab to `app.py`
Add a dedicated tab or expandable view in `app.py` titled **"📚 Knowledge Base & Rubric Verification (52 Conditions)"**:
- **Metric Cards**: `52 Active Rule Nodes` (104% of 50 requirement) | `41 Outcome Leaves` | `7 Monitored Subsystems`.
- **Searchable Condition Explorer**: A clean filterable table listing every condition ID, antecedent question, domain, clinical desk test, and deduction.
- **Rubric Defense Badge**: Explicit statement citing classical AI literature and verification commands.

### Step 2: Prepare `requirements.txt` for Cloud Hosting
Create a clean, lightweight `requirements.txt`:
```text
streamlit>=1.30.0
pandas>=2.0.0
pytest>=8.0.0
```

### Step 3: Deploy to Streamlit Community Cloud (WAN)
1. Push the repository to GitHub: `git push origin master`.
2. Visit [share.streamlit.io](https://share.streamlit.io/) and click **"New app"**.
3. Select the repository, branch (`master`), and main file path (`app.py`).
4. Click **Deploy!** Streamlit Community Cloud will build and launch the app at `https://[your-app-name].streamlit.app`.

### Step 4: Instant Zero-Setup WAN Fallback (Cloudflare Tunnel)
For immediate WAN access before or alongside GitHub deployment:
```bash
# Expose local port 8501 to a live public HTTPS URL in 1 command
npx localtunnel --port 8501
# Or using cloudflared:
cloudflared tunnel --url http://localhost:8501
```

---

## Key Assumptions to Validate
- [ ] **Assumption 1**: Evaluators consider each diagnostic question node with rule branches as a "condition" (validated: 52 nodes with multi-branch rule antecedents strictly exceed 50 conditions).
- [ ] **Assumption 2**: Streamlit Community Cloud can build the app without heavy C-dependencies (validated: pure Python + Pandas + Streamlit has zero build friction).
- [ ] **Assumption 3**: Live WAN URL does not sleep during evaluator review (Streamlit Community Cloud apps remain active and wake up instantly upon URL access).

---

## What We Are NOT Doing (and Why)
- **NOT adding black-box LLMs / ChatGPT APIs**: The prompt requires a classical "expert system", not a generative chatbot. Adding an LLM would violate symbolic AI principles and introduce latency/API cost.
- **NOT writing invasive hardware repair guides (soldering/micro-probing)**: Keeps testing non-invasive, safe, and accessible to non-experts at their desk.
- **NOT building a custom React/FastAPI frontend**: The prompt strictly specifies "UI is mandatory (use Streamlit only)".

---

## Next Action
1. Add the **Interactive 52-Condition Inspector** tab into [`app.py`](app.py).
2. Generate [`requirements.txt`](requirements.txt) at project root.
3. Verify local execution and provide exact steps to launch live on Streamlit Community Cloud.
