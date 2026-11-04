import pytest
from engine import ExpertInferenceEngine, DiagnosticResult


@pytest.fixture
def engine():
    return ExpertInferenceEngine()


def test_mycin_certainty_combination_math(engine):
    """Test standard MYCIN certainty factor formula: CF_combined = CF1 + CF2 * (1 - CF1)."""
    # Combining 0.8 and 0.5: 0.8 + 0.5 * 0.2 = 0.9
    res = engine.combine_certainties(0.8, 0.5)
    assert res == 0.9

    # Commutativity: combine(A, B) == combine(B, A)
    res_comm = engine.combine_certainties(0.5, 0.8)
    assert res == res_comm

    # Boundary cases: with 1.0
    assert engine.combine_certainties(1.0, 0.5) == 1.0
    assert engine.combine_certainties(0.5, 1.0) == 1.0

    # Boundary cases: with 0.0
    assert engine.combine_certainties(0.0, 0.7) == 0.7
    assert engine.combine_certainties(0.7, 0.0) == 0.7

    # Clamping tests
    assert engine.combine_certainties(1.5, 0.5) == 1.0
    assert engine.combine_certainties(-0.5, 0.4) == 0.4


def test_deterministic_leaf_resolution(engine):
    """Test that direct physical evidence leaves resolve with is_deterministic=True and CF >= 0.95."""
    # Battery bulge path: q_emergency_triage -> q_power_state -> q_charging_behavior -> q_battery_bulge
    history = [
        ("q_emergency_triage", "power"),
        ("q_power_state", "turns_on_normal"),
        ("q_charging_behavior", "instant_shutoff_unplug"),
    ]
    step = engine.process_emergency_step(history)
    assert step["status"] == "concluded"
    result: DiagnosticResult = step["result"]
    assert result.is_deterministic is True
    assert result.confidence_score >= 0.95
    assert result.is_inconclusive is False
    assert result.limitation_notes is None


def test_conditional_leaf_resolution_with_hypotheses(engine):
    """Test that ambiguous leaves resolve as conditional with ranked competing hypotheses."""
    # Short circuit / power rail trip path:
    history = [
        ("q_emergency_triage", "power"),
        ("q_power_state", "turns_on_then_dies"),
    ]
    step = engine.process_emergency_step(history)
    assert step["status"] == "concluded"
    result: DiagnosticResult = step["result"]
    assert result.is_deterministic is False
    assert 0.60 <= result.confidence_score < 1.0
    assert len(result.competing_hypotheses) > 0

    for hyp in result.competing_hypotheses:
        assert "title" in hyp
        assert "confidence" in hyp
        assert "differentiator" in hyp
        assert 0.0 <= hyp["confidence"] <= 1.0


def test_tree_audit_critical_intercept_preserves_certainty(engine):
    """Verify that critical intercept in tree audit properly populates certainty metadata."""
    state, step = engine.start_tree_audit()
    # Trigger critical intercept with turns_on_then_dies
    step = engine.advance_tree_audit(state, action="answer", answer_key="turns_on_then_dies")
    assert step.status == "critical_intercept"

    # Terminate critical
    term_step = engine.advance_tree_audit(state, action="terminate_critical")
    assert term_step.status == "concluded_early"
    result: DiagnosticResult = term_step.result
    assert result.confidence_score == 0.85
    assert result.is_deterministic is False
    assert len(result.competing_hypotheses) == 3
