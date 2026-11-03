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
            print(f"Urgency:             [{res.urgency.upper()}]")
            print(f"Estimated Cost:      {res.estimated_cost}")
            print(f"DIY Friendly:        {'Yes (User Serviceable)' if res.diy_friendly else 'No (Professional Board Tech Required)'}")
            print(f"\nRoot Cause:\n{res.issue}")
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


def run_audit_cli(engine: ExpertInferenceEngine, quick_healthy: bool = False):
    print("\n--- [🔍 50-Point Subsystem Hardware Audit] ---")
    print("Systematic inspection across Power, Display, Thermals, Boot, RAM, and Ports.\n")

    questions = engine.get_audit_questions()
    answers = {}

    current_cat = None
    for idx, q in enumerate(questions, 1):
        cat_name = engine.categories.get(q["category"], q["category"])
        if cat_name != current_cat:
            current_cat = cat_name
            print(f"\n>>> Category: {current_cat.upper()} <<<")

        print(f"\n[{idx}/52] {q['title']}: {q['question']}")
        opts = q["options"]
        for opt_idx, opt in enumerate(opts, 1):
            health_tag = "✓ Healthy" if opt.get("is_healthy", True) else f"⚠ Penalty -{opt.get('penalty', 0)}"
            print(f"  ({opt_idx}) {opt['label']} [{health_tag}]")

        if quick_healthy:
            # Default to first healthy option
            healthy_opt = next((o for o in opts if o.get("is_healthy", True)), opts[0])
            answers[q["id"]] = healthy_opt["key"]
            print(f"  -> Selected default: {healthy_opt['label']}")
            continue

        while True:
            choice = input(f"Choose [1-{len(opts)}] (Enter for 1): ").strip()
            if not choice:
                choice = "1"
            if choice.isdigit() and 1 <= int(choice) <= len(opts):
                chosen_opt = opts[int(choice) - 1]
                answers[q["id"]] = chosen_opt["key"]
                break
            print("Invalid input.")

    scorecard: AuditScorecard = engine.evaluate_audit(answers)
    print("\n" + "=" * 65)
    print("📊 50-POINT AUDIT SCORECARD COMPLETE")
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
        print("\n✓ No defects detected! System is in immaculate operational condition.")
    print("=" * 65 + "\n")


def main():
    parser = argparse.ArgumentParser(description="LapDoc - Laptop Diagnostic Expert System")
    parser.add_argument("--emergency", action="store_true", help="Launch directly into Emergency Fast-Triage")
    parser.add_argument("--audit", action="store_true", help="Launch directly into 50-Point Audit")
    parser.add_argument("--audit-quick", action="store_true", help="Run 50-Point Audit with healthy defaults for quick check")
    args = parser.parse_args()

    engine = ExpertInferenceEngine()
    print_banner()

    if args.emergency:
        run_emergency_cli(engine)
        return
    elif args.audit:
        run_audit_cli(engine, quick_healthy=False)
        return
    elif args.audit_quick:
        run_audit_cli(engine, quick_healthy=True)
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
            run_audit_cli(engine, quick_healthy=False)
        elif choice == "3":
            run_audit_cli(engine, quick_healthy=True)
        elif choice == "4":
            print("Exiting LapDoc. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid selection.")


if __name__ == "__main__":
    main()
