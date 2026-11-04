import pytest
from engine import ExpertInferenceEngine, DiagnosticResult


@pytest.fixture
def engine():
    return ExpertInferenceEngine()


def test_legacy_diagnostic_result_backward_compatibility():
    """Verify that DiagnosticResult can still be instantiated with legacy positional/keyword args."""
    diag = DiagnosticResult(
        title="Test Diagnosis",
        issue="Test Issue",
        remediation=["Step 1", "Step 2"],
        urgency="High",
        diy_friendly=True,
        estimated_cost="$50",
    )
    assert diag.confidence_score == 1.0
    assert diag.is_deterministic is True
    assert diag.is_inconclusive is False
    assert diag.competing_hypotheses == []
    assert diag.limitation_notes is None


def test_inconclusive_threshold_trigger(engine, monkeypatch):
    """Verify that when certainty falls below certainty_threshold, is_inconclusive is flagged."""
    # Temporarily set high threshold of 0.90
    engine.certainty_threshold = 0.90

    # Path with 0.85 CF (turns_on_then_dies)
    history = [
        ("q_emergency_triage", "power"),
        ("q_power_state", "turns_on_then_dies"),
    ]
    step = engine.process_emergency_step(history)
    assert step["status"] == "concluded"
    result: DiagnosticResult = step["result"]
    assert result.confidence_score == 0.85
    assert result.is_inconclusive is True
    assert result.limitation_notes is not None
    assert "below the 90% decision threshold" in result.limitation_notes


def test_domain_boundary_detection(engine):
    """Test detection of out-of-scope peripheral and micro-soldering scenarios."""
    # Printer query
    res_printer = engine.check_domain_boundary("My HP LaserJet printer has paper jam and toner smudge")
    assert res_printer is not None
    assert res_printer["in_scope"] is False
    assert "Printer/scanner" in res_printer["reason"]

    # Micro-soldering query
    res_solder = engine.check_domain_boundary("Laptop needs BGA reballing and oscilloscope probe on VCore rail")
    assert res_solder is not None
    assert res_solder["in_scope"] is False
    assert "Component-Level Board Surgery" in res_solder["reason"]

    # In-scope normal hardware symptom
    res_normal = engine.check_domain_boundary("Laptop screen has lines and battery won't charge")
    assert res_normal is None


def test_healthy_branch_baseline_defaults(engine):
    """Verify terminal node without leaf provides sensible baseline certainty without limitation errors."""
    engine.nodes["q_test_terminal"] = {
        "id": "q_test_terminal",
        "category": "power_battery",
        "title": "Test Terminal",
        "question": "Terminal question?",
        "why": "Testing terminal fallback",
        "options": [
            {"key": "all_good", "label": "All good", "is_healthy": True}
        ]
    }
    history = [("q_test_terminal", "all_good")]
    step = engine.process_emergency_step(history)
    assert step["status"] == "concluded"
    result: DiagnosticResult = step["result"]
    assert result.is_inconclusive is False
    assert result.confidence_score == 0.90
    assert "No Hardware Fault Detected" in result.title
