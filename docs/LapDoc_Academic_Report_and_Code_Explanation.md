# LapDoc: A Declarative Symbolic AI Expert System
## Academic Evaluation, Architecture Specification, and Code Implementation Dossier

**Author**: LapDoc Research & Engineering Team  
**Domain**: Computer Hardware Fault Triage & Subsystem Diagnostics  
**Paradigm**: Classical Symbolic Artificial Intelligence (Knowledge-Based Expert System)  
**Reference Codebase**: [LapDoc Repository](file:///home/afzal/Projects/laptop-expert-system)  
**Compiled Artifact**: [LapDoc_Academic_Report_and_Code_Explanation.pdf](file:///home/afzal/Projects/laptop-expert-system/docs/LapDoc_Academic_Report_and_Code_Explanation.pdf)

---

## 1. Executive Summary & Abstract
LapDoc is a classical Knowledge-Based Expert System (KBES) developed for component-level fault isolation, electrical safety verification, and subsystem health scoring in portable personal computers.

When evaluators or examiners ask: *"Is LapDoc really an Artificial Intelligence Expert System, or is it just a hardcoded decision tree / wizard?"*, the answer is:

> **LapDoc is an authentic Knowledge-Based Expert System.** It adheres strictly to the canonical 5-component architecture established by Buchanan, Shortliffe, and Feigenbaum, enforcing complete separation of declarative domain knowledge (`knowledge_base.json`) from procedural inference (`engine.py`).

---

## 2. Theoretical Foundations of Expert Systems
A classical Expert System consists of five interconnected subsystems:
1. **Knowledge Base (KB)**: Declarative domain facts, symptoms, remediations, and certainty factors (`knowledge_base.json`).
2. **Inference Engine**: Domain-independent reasoning algorithms (`engine.py`).
3. **Working Memory**: Dynamic session state holding asserted facts.
4. **Explanation Facility**: Dynamic answering of "Why" and "How" (`explain_question()`, `history_trace`).
5. **User Interface**: Decoupled presentation layer (`app.py`, `cli.py`).

---

## 3. Procedural Script vs. True Symbolic Expert System
| Dimension | Simple Procedural Script / Wizard | LapDoc Symbolic Expert System |
| :--- | :--- | :--- |
| **Separation of Knowledge & Engine** | ❌ None. Rules embedded in `if/else` statements. | ✅ Complete. Zero hardware facts in `engine.py`. |
| **Reasoning Flexibility** | ❌ Single rigid path from root to leaf. | ✅ Dual reasoning modes: Priority DAG Early-Exit + Cascading Gateway Subsystem Tree. |
| **Explanation Facility** | ❌ None or hardcoded console prints. | ✅ Dynamic inspection of active hypothesis ("Why") and deduction path ("How"). |
| **Extensibility** | ❌ Editing rules requires altering code. | ✅ Domain experts add rules in JSON without touching code. |
| **Uncertainty & Inexact Knowledge** | ❌ Binary (Yes/No only). | ✅ Certainty Factors ($CF$) differentiate hard facts from conditional hypotheses. |
| **Boundary Awareness** | ❌ Fails silently or gives wrong leaf. | ✅ Explicit boundary rules; flags inconclusive results ($CF < 0.60$). |

---

## 4. Inexact Reasoning & Certainty Factor Calculus
LapDoc uses the Shortliffe & Buchanan (1975) Certainty Factor formula to combine independent positive corroborating evidence:

$$CF_{combined}(CF_1, CF_2) = CF_1 + CF_2 \cdot (1.0 - CF_1)$$

- **Deterministic Facts ($CF = 1.0$)**: e.g., fractured DC jack pin, visibly swollen battery.
- **Conditional Hypotheses ($0.60 \le CF < 1.0$)**: e.g., faint desktop image under flashlight ($CF = 0.95$).
- **Inconclusive Diagnoses ($CF < 0.60$)**: Flags ambiguous symptoms and recommends lab bench isolation.

---

## 5. Limitation Awareness: "Knowing What It Knows"
1. **Domain Envelope**: Strictly bounded to non-invasive portable PC electrical and subsystem triage. Out-of-scope issues (liquid spill onto multi-layer motherboard) halt triage immediately.
2. **Confidence Threshold**: Any deduction path yielding $CF < 0.60$ is flagged as inconclusive.
3. **Graceful Fallback**: Outputs OEM baseline guidance rather than fabricating guesses.

---

## 6. Viva Defense & Evaluator FAQ
- **Q1: Isn't an expert system obsolete now that we have LLMs?**  
  *Answer*: No. LLMs suffer from probabilistic hallucinations and lack verifiable causal reasoning. In safety-critical hardware diagnostics, zero-hallucination guarantees, formal audit trails, and deterministic safety rules are mandatory.
- **Q2: What makes the knowledge base declarative?**  
  *Answer*: `knowledge_base.json` contains declarative rules. `engine.py` contains zero laptop-specific rules. Swapping JSON allows diagnosing automobiles or medical devices without editing Python code.
- **Q3: How does the system handle uncertainty?**  
  *Answer*: Uses MYCIN certainty factor propagation, ranks competing hypotheses, and flags scores under 60% as inconclusive.

---

## 7. Core Annotated Code References
- `engine.py:54-620`: `ExpertInferenceEngine` definition and traversal methods.
- `engine.py:76-84`: `combine_certainties(cf1, cf2)` MYCIN calculus.
- `engine.py:152-240`: `process_emergency_step()` forward chaining and early-exit leaf resolution.
- `engine.py:298-375`: `evaluate_audit()` multi-subsystem scoring and defect aggregation.

---

## 8. Academic References
1. Shortliffe, E. H., & Buchanan, B. G. (1975). *A model of inexact reasoning in medicine*.
2. Buchanan, B. G., & Shortliffe, E. H. (1984). *Rule-Based Expert Systems: The MYCIN Experiments*.
3. Russell, S., & Norvig, P. (2020). *Artificial Intelligence: A Modern Approach* (4th ed.).
4. Jackson, P. (1999). *Introduction to Expert Systems* (3rd ed.).
