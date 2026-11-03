import pytest
from engine import ExpertInferenceEngine, TreeAuditStepResult, DiagnosticResult, AuditScorecard


@pytest.fixture
def engine():
    return ExpertInferenceEngine()


def test_start_tree_audit(engine):
    state, step_res = engine.start_tree_audit()
    assert step_res.status == "in_progress"
    assert step_res.subsystem_index == 0
    assert step_res.subsystem_key == "power_battery"
    assert step_res.depth_level == 1
    assert step_res.current_node["id"] == "q_power_state"


def test_tree_audit_critical_intercept_and_terminate(engine):
    """Verify that answering with a critical failure triggers intercept and can terminate early."""
    state, step_res = engine.start_tree_audit()

    # Step 1: Power -> turns_on_then_dies (Short circuit leaf)
    res = engine.advance_tree_audit(state, action="answer", answer_key="turns_on_then_dies")
    assert res.status == "critical_intercept"
    assert res.critical_leaf is not None
    assert "Short Circuit" in res.critical_leaf["title"]

    # Terminate early
    concluded = engine.advance_tree_audit(state, action="terminate_critical")
    assert concluded.status == "concluded_early"
    assert isinstance(concluded.result, DiagnosticResult)
    assert "Short Circuit" in concluded.result.title
    assert concluded.result.urgency == "Critical"


def test_tree_audit_critical_intercept_and_continue(engine):
    """Verify that user can choose to continue after a critical intercept to the next subsystem."""
    state, step_res = engine.start_tree_audit()

    # Hit critical short circuit in Subsystem 0 (Power)
    res = engine.advance_tree_audit(state, action="answer", answer_key="turns_on_then_dies")
    assert res.status == "critical_intercept"

    # User chooses to continue auditing
    cont_res = engine.advance_tree_audit(state, action="continue_critical")
    assert cont_res.status == "in_progress"
    assert cont_res.subsystem_index == 1
    assert cont_res.subsystem_key == "display_graphics"
    assert cont_res.depth_level == 1
    assert cont_res.current_node["id"] == "q_display_illumination"


def test_tree_audit_full_completion(engine):
    """Verify traversing all 7 subsystems to completion."""
    state, step_res = engine.start_tree_audit()

    # Loop through answering healthy options until concluded_full
    iterations = 0
    while step_res.status == "in_progress" and iterations < 50:
        iterations += 1
        curr_node = step_res.current_node
        # Choose healthy option
        healthy_opt = next((o for o in curr_node["options"] if o.get("is_healthy", True)), curr_node["options"][0])
        step_res = engine.advance_tree_audit(state, action="answer", answer_key=healthy_opt["key"])
        if step_res.status == "critical_intercept":
            # If any intercept, continue
            step_res = engine.advance_tree_audit(state, action="continue_critical")

    assert step_res.status == "concluded_full"
    assert isinstance(step_res.scorecard, AuditScorecard)
    assert step_res.scorecard.total_score >= 85
    assert len(step_res.trace) >= 7
