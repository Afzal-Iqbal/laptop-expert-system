import pytest
from engine import ExpertInferenceEngine, DiagnosticResult, AuditScorecard

@pytest.fixture
def engine():
    return ExpertInferenceEngine()

def test_engine_initialization(engine):
    assert engine.emergency_entry == "q_emergency_triage"
    assert len(engine.nodes) >= 50
    assert len(engine.categories) >= 6

def test_explanation_facility(engine):
    explanation = engine.explain_question("q_power_state")
    assert "power" in explanation.lower() or "rail" in explanation.lower()

def test_emergency_fast_exit_short_circuit(engine):
    """Verifies that an acute short-circuit powers off diagnosis resolves in just 2 questions."""
    history = [
        ("q_emergency_triage", "power"),
        ("q_power_state", "turns_on_then_dies")
    ]
    step_result = engine.process_emergency_step(history)
    assert step_result["status"] == "concluded"
    res: DiagnosticResult = step_result["result"]
    assert "Short Circuit" in res.title
    assert res.urgency == "Critical"
    assert len(step_result["trace"]) == 2

def test_emergency_backlight_fuse_path(engine):
    """Verifies flashlight test path resolves in 3 questions."""
    history = [
        ("q_emergency_triage", "display"),
        ("q_display_illumination", "screen_completely_dark"),
        ("q_flashlight_test", "faint_image_seen")
    ]
    step_result = engine.process_emergency_step(history)
    assert step_result["status"] == "concluded"
    res: DiagnosticResult = step_result["result"]
    assert "Backlight" in res.title
    assert len(res.remediation) > 0
    assert len(step_result["trace"]) == 3

def test_audit_evaluation_pristine(engine):
    """Verifies an audit with all healthy answers scores A+."""
    audit_questions = engine.get_audit_questions()
    # Choose healthy option (index 0 or is_healthy=True)
    answers = {}
    for q in audit_questions:
        healthy_opt = next(opt for opt in q["options"] if opt.get("is_healthy", True))
        answers[q["id"]] = healthy_opt["key"]

    scorecard: AuditScorecard = engine.evaluate_audit(answers)
    assert scorecard.total_score >= 95
    assert scorecard.letter_grade == "A+"
    assert len(scorecard.flagged_defects) == 0
    assert scorecard.total_estimated_repair_min == 0

def test_audit_evaluation_with_critical_defects(engine):
    """Verifies that critical defects penalize score and flag defects."""
    answers = {
        "q_battery_bulge": "swollen_battery",
        "q_display_illumination": "screen_completely_dark"
    }
    scorecard: AuditScorecard = engine.evaluate_audit(answers)
    assert len(scorecard.flagged_defects) >= 2
    assert scorecard.total_estimated_repair_max > 0
    assert any(d["severity"] == "CRITICAL" for d in scorecard.flagged_defects)
    assert scorecard.letter_grade in ["D", "F"]
