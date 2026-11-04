import json
import os
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any


@dataclass
class DiagnosticResult:
    title: str
    issue: str
    remediation: List[str]
    urgency: str
    diy_friendly: bool
    estimated_cost: str
    history_trace: List[Dict[str, Any]] = field(default_factory=list)
    confidence_score: float = 1.0
    is_deterministic: bool = True
    is_inconclusive: bool = False
    competing_hypotheses: List[Dict[str, Any]] = field(default_factory=list)
    limitation_notes: Optional[str] = None


@dataclass
class AuditScorecard:
    total_score: int
    letter_grade: str
    verdict: str
    category_scores: Dict[str, int]
    flagged_defects: List[Dict[str, Any]]
    total_estimated_repair_min: int
    total_estimated_repair_max: int
    summary_markdown: str


@dataclass
class TreeAuditStepResult:
    status: str  # "in_progress", "critical_intercept", "concluded_early", "concluded_full"
    current_node: Optional[Dict[str, Any]] = None
    subsystem_index: int = 0
    subsystem_key: str = ""
    subsystem_name: str = ""
    depth_level: int = 1
    critical_leaf: Optional[Dict[str, Any]] = None
    result: Optional[DiagnosticResult] = None
    scorecard: Optional[AuditScorecard] = None
    trace: List[Dict[str, Any]] = field(default_factory=list)


class ExpertInferenceEngine:
    def __init__(self, kb_path: Optional[str] = None):
        if kb_path is None:
            kb_path = os.path.join(os.path.dirname(__file__), "knowledge_base.json")
        with open(kb_path, "r", encoding="utf-8") as f:
            self.data = json.load(f)

        self.metadata = self.data["metadata"]
        self.nodes = self.data["nodes"]
        self.emergency_entry = self.data.get("emergency_entry_node", "q_emergency_triage")
        self.categories = self.metadata.get("categories", {})
        self.pipeline = self.metadata.get("subsystem_pipeline", list(self.categories.keys()))
        self.gateways = self.metadata.get("subsystem_gateways", {})
        self.boundary_rules = self.metadata.get("boundary_rules", {
            "certainty_threshold": 0.60,
            "domain": "Non-invasive electronic hardware triage and subsystem diagnostics for portable PCs",
            "out_of_scope_conditions": [],
            "limitation_statement": "If symptoms exceed non-invasive testing or fall below the 60% confidence threshold, physical bench instruments are required."
        })
        self.certainty_threshold = self.boundary_rules.get("certainty_threshold", 0.60)

    @staticmethod
    def combine_certainties(cf1: float, cf2: float) -> float:
        """
        MYCIN standard certainty combination for positive independent evidence:
        CF_combined = CF1 + CF2 * (1 - CF1)
        Clamped to [0.0, 1.0].
        """
        cf1 = max(0.0, min(1.0, float(cf1)))
        cf2 = max(0.0, min(1.0, float(cf2)))
        return round(cf1 + cf2 * (1.0 - cf1), 4)

    def get_node(self, node_id: str) -> Optional[Dict[str, Any]]:
        return self.nodes.get(node_id)

    def explain_question(self, node_id: str) -> str:
        node = self.get_node(node_id)
        if not node:
            return "Node not found in knowledge base."
        return node.get("why", "Diagnosing system state based on observed symptoms.")

    def get_audit_questions(self) -> List[Dict[str, Any]]:
        """Returns all questions excluding the root emergency triage node, grouped by category."""
        return [node for nid, node in self.nodes.items() if nid != "q_emergency_triage"]

    def process_emergency_step(self, history: List[tuple[str, str]]) -> Dict[str, Any]:
        """
        Takes a sequence of (node_id, selected_option_key) pairs and advances the inference state.
        Returns either:
          {"status": "in_progress", "current_node": node_dict, "trace": list_of_steps}
          or
          {"status": "concluded", "result": DiagnosticResult, "trace": list_of_steps}
        """
        if not history:
            entry_node = self.get_node(self.emergency_entry)
            return {
                "status": "in_progress",
                "current_node": entry_node,
                "trace": []
            }

        trace = []
        current_node_id = self.emergency_entry

        for i, (node_id, chosen_key) in enumerate(history):
            node = self.get_node(node_id)
            if not node:
                raise ValueError(f"Invalid node '{node_id}' in history")

            # Find matching option
            selected_option = next((opt for opt in node["options"] if opt["key"] == chosen_key), None)
            if not selected_option:
                raise ValueError(f"Option key '{chosen_key}' not valid for node '{node_id}'")

            trace_step = {
                "step": i + 1,
                "node_id": node_id,
                "title": node["title"],
                "question": node["question"],
                "chosen_label": selected_option["label"],
                "why": node["why"],
                "is_healthy": selected_option.get("is_healthy", False),
            }
            trace.append(trace_step)

            # Check if this choice immediately resolves to a leaf diagnosis
            leaf = selected_option.get("leaf_diagnosis")
            if leaf:
                cf = leaf.get("certainty_factor", 1.0)
                is_det = leaf.get("is_deterministic", True)
                competing = leaf.get("competing_hypotheses", [])
                is_inconclusive = cf < self.certainty_threshold
                limitation_notes = (
                    f"Certainty ({int(cf*100)}%) is below the {int(self.certainty_threshold*100)}% decision threshold. "
                    f"Symptoms remain ambiguous; lab bench isolation recommended."
                    if is_inconclusive else None
                )

                result = DiagnosticResult(
                    title=leaf["title"],
                    issue=leaf["issue"],
                    remediation=leaf["remediation"],
                    urgency=leaf.get("urgency", "High"),
                    diy_friendly=leaf.get("diy_friendly", False),
                    estimated_cost=selected_option.get("estimated_cost_usd", "Varies"),
                    history_trace=trace,
                    confidence_score=cf,
                    is_deterministic=is_det,
                    is_inconclusive=is_inconclusive,
                    competing_hypotheses=competing,
                    limitation_notes=limitation_notes
                )
                return {
                    "status": "concluded",
                    "result": result,
                    "trace": trace
                }

            # Otherwise, follow next_question pointer
            next_q = selected_option.get("next_question")
            if next_q:
                current_node_id = next_q
            else:
                # Terminal node reached without a specific fault leaf (subsystem branch completed normally)
                node_cat = node.get("category", "")
                cat_label = self.categories.get(node_cat, node_cat.replace("_", " ").title())
                result = DiagnosticResult(
                    title=f"No Hardware Fault Detected in {cat_label}",
                    issue=f"All diagnostic checks for {cat_label} were evaluated within normal OEM operating parameters. If symptoms persist, the issue is likely software/driver related or located in an adjacent subsystem.",
                    remediation=[
                        f"Hardware in {cat_label} appears operational.",
                        "Reboot into Windows Safe Mode or clean boot to isolate background third-party software/drivers.",
                        "If experiencing crashes or anomalies, run OS file verification (`sfc /scannow`).",
                        "Run the full 50-Point Audit to systematically inspect all other laptop subsystems."
                    ],
                    urgency="Routine",
                    diy_friendly=True,
                    estimated_cost="$0",
                    history_trace=trace,
                    confidence_score=0.90,
                    is_deterministic=False,
                    is_inconclusive=False,
                    competing_hypotheses=[],
                    limitation_notes=None
                )
                return {
                    "status": "concluded",
                    "result": result,
                    "trace": trace
                }

        next_node = self.get_node(current_node_id)
        return {
            "status": "in_progress",
            "current_node": next_node,
            "trace": trace
        }

    def evaluate_audit(self, answers: Dict[str, str]) -> AuditScorecard:
        """
        Evaluates answers across all 52 audit checks.
        answers: {node_id: option_key}
        """
        category_penalties: Dict[str, int] = {cat: 0 for cat in self.categories.keys()}
        category_max_points: Dict[str, int] = {cat: 0 for cat in self.categories.keys()}
        flagged_defects: List[Dict[str, Any]] = []
        cost_min_total = 0
        cost_max_total = 0

        for nid, node in self.nodes.items():
            if nid == "q_emergency_triage":
                continue
            cat = node.get("category", "other")
            if cat not in category_penalties:
                category_penalties[cat] = 0
                category_max_points[cat] = 0

            chosen_key = answers.get(nid)
            # Default to healthy if unanswered
            matched_opt = next((opt for opt in node["options"] if opt["key"] == chosen_key), None)
            if not matched_opt:
                matched_opt = node["options"][0]

            penalty = matched_opt.get("penalty", 0)
            category_penalties[cat] += penalty
            category_max_points[cat] += 25  # standard theoretical max penalty per question

            if not matched_opt.get("is_healthy", True) or penalty > 0:
                cost_str = matched_opt.get("estimated_cost_usd", "$0")
                min_c, max_c = self._parse_cost_range(cost_str)
                cost_min_total += min_c
                cost_max_total += max_c

                flagged_defects.append({
                    "node_id": nid,
                    "category": self.categories.get(cat, cat.replace("_", " ").title()),
                    "title": node["title"],
                    "question": node["question"],
                    "observed": matched_opt["label"],
                    "defect": matched_opt.get("defect_description", node["title"] + " issue"),
                    "severity": matched_opt.get("severity", "medium").upper(),
                    "penalty": penalty,
                    "cost": cost_str
                })

        # Calculate category scores out of 100
        category_scores = {}
        for cat in self.categories.keys():
            pen = category_penalties.get(cat, 0)
            cat_score = max(0, 100 - (pen * 2))
            category_scores[cat] = cat_score

        # Total overall score
        total_penalty = sum(category_penalties.values())
        overall_score = max(0, min(100, 100 - int(total_penalty * 0.45)))

        # Letter grade & verdict
        grade, verdict = self._determine_grade_and_verdict(overall_score, flagged_defects)

        # Generate summary markdown
        summary_md = self._generate_audit_markdown(overall_score, grade, verdict, flagged_defects, cost_min_total, cost_max_total)

        return AuditScorecard(
            total_score=overall_score,
            letter_grade=grade,
            verdict=verdict,
            category_scores=category_scores,
            flagged_defects=flagged_defects,
            total_estimated_repair_min=cost_min_total,
            total_estimated_repair_max=cost_max_total,
            summary_markdown=summary_md
        )

    def _determine_grade_and_verdict(self, score: int, defects: List[Dict[str, Any]]) -> tuple[str, str]:
        critical_count = sum(1 for d in defects if d.get("severity") == "CRITICAL")
        if critical_count > 0:
            if score < 50:
                return "F", "High Risk / Critical Hardware Failure Present"
            return "D", "Conditional Pass / Major Component Defect Flagged"

        if score >= 95:
            return "A+", "Pristine / Grade A+ Condition (Ready for Purchase)"
        elif score >= 85:
            return "A", "Good Working Condition (Minor Cosmetic Wear Only)"
        elif score >= 75:
            return "B", "Moderate Wear / Subsystems Require Routine Service"
        elif score >= 60:
            return "C", "Fair Condition / Notable Degradation Observed"
        elif score >= 50:
            return "D", "Poor Condition / Substantial Repairs Required"
        else:
            return "F", "Failing Grade / Not Recommended Without Heavy Refurbishment"

    def _parse_cost_range(self, cost_str: str) -> tuple[int, int]:
        matches = re.findall(r"\$(\d+)", cost_str)
        if len(matches) == 2:
            return int(matches[0]), int(matches[1])
        elif len(matches) == 1:
            val = int(matches[0])
            return val, val
        return 0, 0

    def _generate_audit_markdown(self, score: int, grade: str, verdict: str,
                                 defects: List[Dict[str, Any]], cost_min: int, cost_max: int) -> str:
        lines = [
            f"# LapDoc Hardware Audit Scorecard",
            f"**Overall Health Score:** `{score}/100` | **Grade:** `{grade}`",
            f"**Status Verdict:** {verdict}",
            f"**Estimated Total Repair/Refurbishment Cost:** `${cost_min} - ${cost_max}`",
            "",
            "## Flagged Issues & Defects"
        ]
        if not defects:
            lines.append("✓ *No defects detected. All audited subsystems passed operational benchmarks.*")
        else:
            for d in defects:
                lines.append(f"- **[{d['severity']}] {d['title']}** ({d['category']})")
                lines.append(f"  - *Observed:* {d['observed']}")
                lines.append(f"  - *Defect:* {d['defect']}")
                lines.append(f"  - *Estimated Cost:* {d['cost']}")
        return "\n".join(lines)

    def start_tree_audit(self) -> tuple[Dict[str, Any], TreeAuditStepResult]:
        first_sub = self.pipeline[0]
        gateway_node_id = self.gateways.get(first_sub, "q_power_state")
        first_node = self.get_node(gateway_node_id)
        state = {
            "pipeline_index": 0,
            "current_node_id": gateway_node_id,
            "depth_level": 1,
            "answers": {},
            "trace": [],
            "pending_critical": None,
            "critical_intercepted": []
        }
        step_res = TreeAuditStepResult(
            status="in_progress",
            current_node=first_node,
            subsystem_index=0,
            subsystem_key=first_sub,
            subsystem_name=self.categories.get(first_sub, first_sub),
            depth_level=1,
            trace=[]
        )
        return state, step_res

    def advance_tree_audit(self, state: Dict[str, Any], action: str = "answer", answer_key: Optional[str] = None) -> TreeAuditStepResult:
        if action == "terminate_critical":
            critical = state.get("pending_critical") or {}
            cf = critical.get("certainty_factor", 1.0)
            is_det = critical.get("is_deterministic", True)
            competing = critical.get("competing_hypotheses", [])
            is_inconclusive = cf < self.certainty_threshold
            limitation_notes = (
                f"Certainty ({int(cf*100)}%) is below the {int(self.certainty_threshold*100)}% decision threshold. "
                f"Physical bench testing recommended."
                if is_inconclusive else None
            )
            diag = DiagnosticResult(
                title=critical.get("title", "Critical Hardware Defect"),
                issue=critical.get("issue", "A critical hardware fault was detected requiring immediate shutdown or service."),
                remediation=critical.get("remediation", ["Seek certified technician board repair."]),
                urgency=critical.get("urgency", "Critical"),
                diy_friendly=critical.get("diy_friendly", False),
                estimated_cost=critical.get("cost", "Varies"),
                history_trace=state.get("trace", []),
                confidence_score=cf,
                is_deterministic=is_det,
                is_inconclusive=is_inconclusive,
                competing_hypotheses=competing,
                limitation_notes=limitation_notes
            )
            return TreeAuditStepResult(
                status="concluded_early",
                result=diag,
                trace=state.get("trace", [])
            )

        if action == "continue_critical":
            critical = state.get("pending_critical")
            if critical:
                state["critical_intercepted"].append(critical)
                state["pending_critical"] = None

            state["pipeline_index"] += 1
            return self._advance_to_next_subsystem_or_conclude(state)

        if action == "answer":
            if not answer_key:
                raise ValueError("answer_key is required when action is 'answer'")

            node = self.get_node(state["current_node_id"])
            if not node:
                raise ValueError(f"Invalid current_node_id '{state['current_node_id']}'")

            matched_opt = next((o for o in node["options"] if o["key"] == answer_key), None)
            if not matched_opt:
                raise ValueError(f"Option key '{answer_key}' not valid for node '{node['id']}'")

            state["answers"][node["id"]] = answer_key

            current_sub_key = self.pipeline[state["pipeline_index"]]
            trace_entry = {
                "step": len(state["trace"]) + 1,
                "subsystem": self.categories.get(current_sub_key, current_sub_key),
                "depth": state["depth_level"],
                "node_id": node["id"],
                "title": node["title"],
                "question": node["question"],
                "chosen_label": matched_opt["label"],
                "is_healthy": matched_opt.get("is_healthy", True),
                "why": node.get("why", "")
            }
            state["trace"].append(trace_entry)

            leaf = matched_opt.get("leaf_diagnosis")
            if leaf:
                if leaf.get("urgency") == "Critical":
                    state["pending_critical"] = {
                        **leaf,
                        "cost": matched_opt.get("estimated_cost_usd", "Varies"),
                        "node_title": node["title"],
                        "category": self.categories.get(current_sub_key, current_sub_key)
                    }
                    return TreeAuditStepResult(
                        status="critical_intercept",
                        current_node=node,
                        subsystem_index=state["pipeline_index"],
                        subsystem_key=current_sub_key,
                        subsystem_name=self.categories.get(current_sub_key, current_sub_key),
                        depth_level=state["depth_level"],
                        critical_leaf=state["pending_critical"],
                        trace=state["trace"]
                    )
                else:
                    state["pipeline_index"] += 1
                    return self._advance_to_next_subsystem_or_conclude(state)

            nxt = matched_opt.get("next_question")
            if nxt:
                nxt_node = self.get_node(nxt)
                if nxt_node and nxt_node.get("category") == node.get("category"):
                    state["current_node_id"] = nxt
                    state["depth_level"] += 1
                    return TreeAuditStepResult(
                        status="in_progress",
                        current_node=nxt_node,
                        subsystem_index=state["pipeline_index"],
                        subsystem_key=current_sub_key,
                        subsystem_name=self.categories.get(current_sub_key, current_sub_key),
                        depth_level=state["depth_level"],
                        trace=state["trace"]
                    )
                else:
                    state["pipeline_index"] += 1
                    return self._advance_to_next_subsystem_or_conclude(state)
            else:
                state["pipeline_index"] += 1
                return self._advance_to_next_subsystem_or_conclude(state)

        raise ValueError(f"Unknown action: '{action}'")

    def _advance_to_next_subsystem_or_conclude(self, state: Dict[str, Any]) -> TreeAuditStepResult:
        if state["pipeline_index"] >= len(self.pipeline):
            scorecard = self.evaluate_audit(state["answers"])
            return TreeAuditStepResult(
                status="concluded_full",
                scorecard=scorecard,
                trace=state["trace"]
            )
        else:
            next_sub = self.pipeline[state["pipeline_index"]]
            next_gateway = self.gateways.get(next_sub)
            state["current_node_id"] = next_gateway
            state["depth_level"] = 1
            node = self.get_node(next_gateway)
            return TreeAuditStepResult(
                status="in_progress",
                current_node=node,
                subsystem_index=state["pipeline_index"],
                subsystem_key=next_sub,
                subsystem_name=self.categories.get(next_sub, next_sub),
                depth_level=1,
                trace=state["trace"]
            )

    def check_domain_boundary(self, symptom_text: str) -> Optional[Dict[str, Any]]:
        """
        Evaluates whether a reported symptom scenario exceeds the expert system's domain boundaries.
        Returns a limitation dictionary if out of bounds, or None if within scope.
        """
        text = symptom_text.lower()
        if re.search(r"\b(printer|scanner|paper|cartridge|toner)\b", text):
            return {
                "in_scope": False,
                "reason": "Non-PC Peripheral: Printer/scanner hardware falls outside laptop motherboard & subsystem triage.",
                "recommendation": "Consult dedicated printer diagnostic equipment and documentation."
            }
        if re.search(r"\b(micro-soldering|bga reballing|oscilloscope|layer separation|burnt pcb)\b", text):
            return {
                "in_scope": False,
                "reason": "Component-Level Board Surgery: Issue requires specialized microscopic lab instruments.",
                "recommendation": "Dispatch motherboard to an advanced electronics micro-soldering facility."
            }
        return None


