import argparse
import sys
from engine import ExpertInferenceEngine, DiagnosticResult, AuditScorecard


def print_banner():
    banner = r"""
========================================================================
   _                 ____             
  | |    __ _ _ __  |  _ \  ___   ___ 
  | |   / _` | '_ \ | | | |/ _ \ / __|
  | |__| (_| | |_) || |_| | (_) | (__ 
  |_____\__,_| .__/ |____/ \___/ \___|
             |_|                      
   Laptop Hardware & Firmware Diagnostic Expert System
========================================================================
"""
    print(banner)


def run_emergency_cli(engine: ExpertInferenceEngine):
    print("\n--- [⚡ Emergency Fast-Triage Mode] ---")
    print("Answer questions step-by-step. The system will exit as soon as a root cause is found.\n")

    history = []
    step_num = 1

    while True:
        step_res = engine.process_emergency_step(history)
        status = step_res["status"]

        if status == "concluded":
            res: DiagnosticResult = step_res["result"]
            print("\n" + "=" * 65)
            print(f"🎯 DIAGNOSIS CONCLUDED: {res.title}")
            print("=" * 65)
            conf_percent = int(res.confidence_score * 100)
            det_label = "DETERMINISTIC (Physical Proof)" if res.is_deterministic else "CONDITIONAL (Heuristic Hypothesis)"
            print(f"Certainty Factor:    {conf_percent}% [{det_label}]")
            print(f"Urgency:             [{res.urgency.upper()}]")
            print(f"Estimated Cost:      {res.estimated_cost}")
            print(f"DIY Friendly:        {'Yes (User Serviceable)' if res.diy_friendly else 'No (Professional Board Tech Required)'}")

            if res.is_inconclusive or res.limitation_notes:
                print("\n" + "!" * 65)
                print("⚠️  SYSTEM LIMITATION WARNING:")
                print(f"   {res.limitation_notes}")
                print("!" * 65)

            print(f"\nRoot Cause:\n{res.issue}")

            if res.competing_hypotheses:
                print("\n--- [Differential Diagnoses / Competing Hypotheses] ---")
                for h_idx, hyp in enumerate(res.competing_hypotheses, 1):
                    hyp_conf = int(hyp.get("confidence", 0) * 100)
                    print(f"  {h_idx}. {hyp['title']} ({hyp_conf}% certainty)")
                    print(f"     Differentiator: {hyp.get('differentiator', 'N/A')}")

            print("\nStep-by-Step Remediation Plan:")
            for idx, step in enumerate(res.remediation, 1):
                print(f"  {idx}. {step}")

            print("\n--- [Inference Trace: How This Was Derived] ---")
            for t in res.history_trace:
                print(f"  Step {t['step']}: {t['title']} -> Selected: '{t['chosen_label']}'")
            print("=" * 65 + "\n")
            break

        node = step_res["current_node"]
        print(f"\n[Step {step_num}] {node['title']}")
        print(f"Question: {node['question']}")
        print(f"💡 Why this is asked: {node['why']}")

        options = node["options"]
        for idx, opt in enumerate(options, 1):
            print(f"  ({idx}) {opt['label']}")

        while True:
            choice = input(f"Select option [1-{len(options)}] or 'q' to quit: ").strip().lower()
            if choice == 'q':
                print("Diagnostic session aborted.")
                return
            if choice.isdigit() and 1 <= int(choice) <= len(options):
                chosen_opt = options[int(choice) - 1]
                history.append((node["id"], chosen_opt["key"]))
                step_num += 1
                break
            print("Invalid input. Please enter a valid number.")


def run_tree_audit_cli(engine: ExpertInferenceEngine, quick_healthy: bool = False):
    print("\n--- [🔍 Cascading Decision-Tree Subsystem Audit] ---")
    print("Hierarchical traversal across all 7 hardware domains with early critical intercept.\n")

    state, step_res = engine.start_tree_audit()

    while True:
        if step_res.status == "critical_intercept":
            crit = step_res.critical_leaf
            print("\n" + "!" * 65)
            print(f"🚨 CRITICAL HARDWARE FAULT DETECTED: {crit['title']}")
            print(f"Subsystem: {step_res.subsystem_name} | Urgency: [{crit.get('urgency', 'CRITICAL')}]")
            print(f"Root Issue: {crit['issue']}")
            print(f"Est. Repair: {crit.get('cost', 'Varies')}")
            print("!" * 65)
            print("\nWhat would you like to do?")
            print("  (1) 🛑 Terminate immediately & generate Emergency Repair Plan")
            print("  (2) ⏩ Continue auditing remaining subsystems")

            if quick_healthy:
                step_res = engine.advance_tree_audit(state, action="continue_critical")
                continue

            while True:
                crit_choice = input("Select [1 or 2]: ").strip()
                if crit_choice == "1":
                    step_res = engine.advance_tree_audit(state, action="terminate_critical")
                    break
                elif crit_choice == "2":
                    step_res = engine.advance_tree_audit(state, action="continue_critical")
                    break
                print("Invalid choice. Please enter 1 or 2.")
            continue

        if step_res.status == "concluded_early":
            res: DiagnosticResult = step_res.result
            print("\n" + "=" * 65)
            print(f"🛑 AUDIT TERMINATED EARLY: {res.title}")
            print("=" * 65)
            conf_percent = int(res.confidence_score * 100)
            det_label = "DETERMINISTIC (Physical Proof)" if res.is_deterministic else "CONDITIONAL (Heuristic Hypothesis)"
            print(f"Certainty Factor:    {conf_percent}% [{det_label}]")
            print(f"Urgency:        [{res.urgency.upper()}]")
            print(f"Est. Cost:      {res.estimated_cost}")

            if res.is_inconclusive or res.limitation_notes:
                print("\n" + "!" * 65)
                print("⚠️  SYSTEM LIMITATION WARNING:")
                print(f"   {res.limitation_notes}")
                print("!" * 65)

            print(f"\nRoot Cause:\n{res.issue}")

            if res.competing_hypotheses:
                print("\n--- [Differential Diagnoses / Competing Hypotheses] ---")
                for h_idx, hyp in enumerate(res.competing_hypotheses, 1):
                    hyp_conf = int(hyp.get("confidence", 0) * 100)
                    print(f"  {h_idx}. {hyp['title']} ({hyp_conf}% certainty)")
                    print(f"     Differentiator: {hyp.get('differentiator', 'N/A')}")

            print("\nStep-by-Step Remediation Plan:")
            for idx, step in enumerate(res.remediation, 1):
                print(f"  {idx}. {step}")
            print("\n--- [Audit Traversal Trace Prior to Termination] ---")
            for t in res.history_trace:
                print(f"  Step {t['step']} ({t['subsystem']}) Depth {t['depth']}: {t['title']} -> '{t['chosen_label']}'")
            print("=" * 65 + "\n")
            break

        if step_res.status == "concluded_full":
            scorecard: AuditScorecard = step_res.scorecard
            print("\n" + "=" * 65)
            print("📊 50-POINT CASCADING AUDIT SCORECARD COMPLETE")
            print("=" * 65)
            print(f"Overall Health Score:  {scorecard.total_score}/100")
            print(f"Letter Grade:          [{scorecard.letter_grade}]")
            print(f"Condition Verdict:     {scorecard.verdict}")
            print(f"Est. Repair Expense:   ${scorecard.total_estimated_repair_min} - ${scorecard.total_estimated_repair_max}")
            print("\nCategory Breakdown:")
            for cat_id, score in scorecard.category_scores.items():
                cat_label = engine.categories.get(cat_id, cat_id)
                print(f"  - {cat_label:<35}: {score:>3}/100")

            if scorecard.flagged_defects:
                print(f"\nFlagged Defects ({len(scorecard.flagged_defects)}):")
                for d in scorecard.flagged_defects:
                    print(f"  • [{d['severity']}] {d['title']}: {d['defect']} (Est: {d['cost']})")
            else:
                print("\n✓ No defects detected! System passed all audited subsystems.")
            print("=" * 65 + "\n")
            break

        node = step_res.current_node
        sub_name = step_res.subsystem_name
        depth = step_res.depth_level
        depth_tag = "Level 1: Gateway Triage" if depth == 1 else f"Level {depth}: Component Deep-Dive"

        print(f"\n[Subsystem {step_res.subsystem_index + 1}/7: {sub_name}] ({depth_tag})")
        print(f"Question: {node['question']}")
        print(f"💡 Why this is asked: {node.get('why', '')}")

        opts = node["options"]
        for opt_idx, opt in enumerate(opts, 1):
            h_tag = "✓ Nominal" if opt.get("is_healthy", True) else f"⚠ Fault / Issue"
            print(f"  ({opt_idx}) {opt['label']} [{h_tag}]")

        if quick_healthy:
            healthy_opt = next((o for o in opts if o.get("is_healthy", True)), opts[0])
            step_res = engine.advance_tree_audit(state, action="answer", answer_key=healthy_opt["key"])
            continue

        while True:
            choice = input(f"Choose [1-{len(opts)}] or 'q' to abort: ").strip().lower()
            if choice == 'q':
                print("Audit aborted.")
                return
            if choice.isdigit() and 1 <= int(choice) <= len(opts):
                chosen_opt = opts[int(choice) - 1]
                step_res = engine.advance_tree_audit(state, action="answer", answer_key=chosen_opt["key"])
                break
            print("Invalid input.")


def main():
    parser = argparse.ArgumentParser(description="LapDoc - Laptop Diagnostic Expert System")
    parser.add_argument("--emergency", action="store_true", help="Launch directly into Emergency Fast-Triage")
    parser.add_argument("--audit", action="store_true", help="Launch directly into Cascading Tree Audit")
    parser.add_argument("--audit-quick", action="store_true", help="Run Cascading Tree Audit with healthy defaults for quick check")
    args = parser.parse_args()

    engine = ExpertInferenceEngine()
    print_banner()

    if args.emergency:
        run_emergency_cli(engine)
        return
    elif args.audit:
        run_tree_audit_cli(engine, quick_healthy=False)
        return
    elif args.audit_quick:
        run_tree_audit_cli(engine, quick_healthy=True)
        return

    while True:
        print("Select Mode:")
        print("  1. ⚡ Emergency Fast-Triage (Early leaf exit in 4-8 steps)")
        print("  2. 🔍 50-Point Subsystem Pre-Purchase Audit (Exhaustive Checklist)")
        print("  3. ⚡ Quick Smoke Audit (Auto-fills healthy checks)")
        print("  4. 🚪 Exit")
        choice = input("\nEnter choice [1-4]: ").strip()

        if choice == "1":
            run_emergency_cli(engine)
        elif choice == "2":
            run_tree_audit_cli(engine, quick_healthy=False)
        elif choice == "3":
            run_tree_audit_cli(engine, quick_healthy=True)
        elif choice == "4":
            print("Exiting LapDoc. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid selection.")


if __name__ == "__main__":
    main()
