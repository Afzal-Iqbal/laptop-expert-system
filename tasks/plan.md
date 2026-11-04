# Implementation Plan: LapDoc Expert System Rigor Upgrade

## Overview
This plan implements the complete specification in [SPEC.md](file:///home/afzal/Projects/laptop-expert-system/SPEC.md). It delivers:
1. A rigorous academic evaluation document (`docs/EXPERT_SYSTEM_EVALUATION.md`) establishing LapDoc's standing against classical AI Expert System literature (MYCIN, DENDRAL, CLIPS, Russell & Norvig).
2. Knowledge base and inference engine upgrades incorporating **Certainty Factors** ($CF \in [0.0, 1.0]$) to differentiate deterministic ("hardcoded") rules from conditional ("may or may not") situations with ranked differential hypotheses.
3. Explicit **Boundary & Limitation Awareness** to detect out-of-scope conditions and low-confidence thresholds.
4. CLI and Streamlit UI integrations displaying confidence metrics and limitation alerts.

---

## Architecture Decisions

1. **Certainty Factor Representation & Mathematics**:
   - Each leaf diagnosis in `knowledge_base.json` specifies an intrinsic `certainty_factor` ($0.0$ to $1.0$).
   - A diagnosis with $CF = 1.0$ is classified as **Deterministic** (absolute physical evidence, e.g. broken pin, visible burn).
   - A diagnosis with $CF < 1.0$ is classified as **Conditional** (probabilistic symptom correlation, e.g. black screen, sudden power cut).
   - Independent positive evidence combines via MYCIN formula:
     $$CF_{combined} = CF_1 + CF_2 \cdot (1 - CF_1)$$
   - Ambiguous nodes provide a `competing_hypotheses` list containing ranked alternative candidates with their respective confidence ratings.

2. **Limitation & Boundary Detection**:
   - A configurable certainty threshold (default $0.60$ / $60\%$). If a diagnostic conclusion has $CF < 0.60$, `DiagnosticResult.is_inconclusive` is set to `True`.
   - Dedicated boundary nodes and rules for out-of-scope issues (e.g. liquid spill needing microscopic board repair, physical chassis damage) return structured limitation notices recommending bench hardware diagnostics.
   - Preserves 100% backward compatibility for all existing callers of `DiagnosticResult`.

3. **Symbolic AI Purity**:
   - Zero black-box ML or LLM dependencies. All reasoning remains 100% transparent, explainable, and verifiable.

---

## Dependency Graph
```text
docs/EXPERT_SYSTEM_EVALUATION.md (Independent documentation)
          │
knowledge_base.json (Add CFs, competing hypotheses, boundary rules)
          │
       engine.py (Certainty calculation, limitation checking, trace enrichment)
          │
    ┌─────┴────────────────┐
    ▼                      ▼
  cli.py                 app.py (Streamlit)
```

---

## Task List

### Phase 1: Academic Defense & Core Engine Upgrade

- [ ] **Task 1: Academic Evaluation & Viva Defense Document**
  - Write `docs/EXPERT_SYSTEM_EVALUATION.md` covering the formal AI expert system taxonomy, comparison to MYCIN/CLIPS, knowledge base vs inference engine separation, working memory, explanation facilities, boundary awareness, and model viva Q&As.

- [ ] **Task 2: Knowledge Base Enrichment with Certainty Factors & Boundary Rules**
  - Update `knowledge_base.json` to equip leaf diagnoses with `certainty_factor`, `is_deterministic`, `competing_hypotheses`, and `boundary_conditions`.
  - Update schema tests in `tests/test_knowledge_base.py`.

- [ ] **Task 3: Inference Engine Uncertainty & Limitation Logic**
  - Update `DiagnosticResult` in `engine.py` with `confidence_score`, `is_deterministic`, `is_inconclusive`, `competing_hypotheses`, and `limitation_notes`.
  - Implement MYCIN certainty combination and boundary threshold evaluations.
  - Create new unit tests in `tests/test_uncertainty.py` and `tests/test_boundary.py`.
  - Maintain backward compatibility so existing tests in `tests/test_engine.py` and `tests/test_tree_audit.py` pass without regression.

### Checkpoint 1: Foundation Verification
- [ ] All 17 existing tests + new unit tests pass cleanly via `.venv/bin/pytest`.
- [ ] Diagnostic traces correctly propagate Certainty Factors and identify limitations.

---

### Phase 2: Interface Enhancements & Final Validation

- [ ] **Task 4: CLI Terminal Integration for Confidence, Hypotheses, & Limitations**
  - Update `cli.py` to format and print certainty percentages, deterministic/conditional tags, competing hypotheses, and limitation alerts.
  - Verify and update `tests/test_cli.py`.

- [ ] **Task 5: Streamlit Web UI Integration for Confidence Meters & Differential Diagnoses**
  - Update `app.py` to render visual certainty progress bars, badge indicators (`Deterministic` vs `Conditional`), expandable differential diagnoses, and boundary warning cards.
  - Verify and update `tests/test_app.py`.

### Checkpoint 2: Final Acceptance
- [ ] 100% test pass across all test modules in `.venv/bin/pytest`.
- [ ] CLI runner operates cleanly across `--emergency`, `--audit`, and `--audit-quick`.
- [ ] Streamlit web app runs without exceptions.

---

## Risks and Mitigations

| Risk | Impact | Mitigation |
| :--- | :---: | :--- |
| **Breaking existing test assertions on `DiagnosticResult`** | High | Default all new fields in `DiagnosticResult` (`confidence_score=1.0`, `is_deterministic=True`, `is_inconclusive=False`, etc.) to maintain total backward compatibility. |
| **Over-complicating knowledge base JSON schema** | Medium | Keep new fields optional with sensible engine fallbacks (if a node lacks `certainty_factor`, default to `1.0`). |
| **UI clutter in Streamlit** | Low | Use Streamlit expanders (`st.expander`) for competing hypotheses and concise alert banners for limitations. |

---

## Open Questions Resolved
- **Certainty Threshold**: Set default to $0.60$ (60%) with explicit note that below 60% requires bench testing.
- **Competing Hypotheses**: Display top 2–3 ranked alternative hypotheses in conditional cases.
