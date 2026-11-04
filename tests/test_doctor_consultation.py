import pytest
from engine import ExpertInferenceEngine, DiagnosticResult


@pytest.fixture
def engine():
    return ExpertInferenceEngine()


def test_get_clinical_test(engine):
    """Verify that nodes with clinical desk tests return valid structured instructions."""
    test_info = engine.get_clinical_test("q_flashlight_test")
    assert test_info is not None
    assert test_info["test_name"] == "Smartphone Flashlight Screen Test"
    assert len(test_info["instructions"]) >= 2
    assert "backlight" in test_info["expected_observation"].lower()

    # Node without clinical test returns None
    assert engine.get_clinical_test("q_emergency_triage") is None
    assert engine.get_clinical_test("non_existent_node") is None


def test_common_ailment_immediate_surety(engine):
    """Verify that common issues resolve with 100% certainty factor and direct prescription."""
    # Emergency triage -> Battery Bulge -> Swollen Battery (Dangerous)
    history = [
        ("q_emergency_triage", "power"),
        ("q_power_state", "turns_on_normal"),
        ("q_charging_behavior", "charges_fine"),
        ("q_battery_discharge", "normal_4h_plus"),
        ("q_battery_bulge", "swollen_battery")
    ]
    res = engine.process_emergency_step(history)
    assert res["status"] == "concluded"
    diag: DiagnosticResult = res["result"]

    assert diag.confidence_score == 1.0
    assert diag.is_deterministic is True
    assert diag.is_common is True
    assert "hazard" in diag.prognosis.lower() or "swollen" in diag.prognosis.lower()
    assert len(diag.prescription) > 0
    assert any("Rx" in p for p in diag.prescription)


def test_clinical_test_captured_in_consultation_trace(engine):
    """Verify that when a clinical test is performed, it is captured in clinical_tests_performed."""
    # Emergency triage -> Display -> Flashlight Test -> Faint Image
    history = [
        ("q_emergency_triage", "display"),
        ("q_display_illumination", "screen_completely_dark"),
        ("q_flashlight_test", "faint_image_seen")
    ]
    res = engine.process_emergency_step(history)
    assert res["status"] == "concluded"
    diag: DiagnosticResult = res["result"]

    # Flashlight test was conducted at step 3
    assert len(diag.clinical_tests_performed) == 1
    test_record = diag.clinical_tests_performed[0]
    assert test_record["test_name"] == "Smartphone Flashlight Screen Test"
    assert "faint" in test_record["observation"].lower()
    assert diag.is_common is True
    assert diag.confidence_score >= 0.95


def test_generate_doctor_report(engine):
    """Verify that generate_doctor_report produces a complete clinical consultation report."""
    history = [
        ("q_emergency_triage", "power"),
        ("q_power_state", "no_life"),
        ("q_charger_led", "charger_led_off")
    ]
    res = engine.process_emergency_step(history)
    assert res["status"] == "concluded"
    diag: DiagnosticResult = res["result"]

    report = engine.generate_doctor_report(diag, brand="Dell XPS 15", processor="Intel Core i7")
    assert report["patient_profile"]["brand"] == "Dell XPS 15"
    assert report["patient_profile"]["processor"] == "Intel Core i7"
    assert "chief_complaint" in report
    assert "diagnosis" in report
    assert report["diagnosis"] == diag.title
    assert "prognosis" in report
    assert isinstance(report["prescription"], list)
    assert len(report["prescription"]) > 0
    assert "surety_label" in report


def test_tree_audit_doctor_protocols(engine):
    """Verify that tree audit critical intercept includes doctor consultation fields."""
    state, step_res = engine.start_tree_audit()

    # Answer turns_on_then_dies (Motherboard short / critical intercept)
    step_res = engine.advance_tree_audit(state, action="answer", answer_key="turns_on_then_dies")
    assert step_res.status == "critical_intercept"

    # Terminate critical and verify DiagnosticResult
    step_res = engine.advance_tree_audit(state, action="terminate_critical")
    assert step_res.status == "concluded_early"
    diag: DiagnosticResult = step_res.result
    assert diag.urgency == "Critical"
    assert len(diag.prescription) > 0
    assert diag.prognosis is not None
