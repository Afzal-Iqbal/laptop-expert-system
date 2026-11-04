import py_compile
import os

def test_app_syntax_and_compilation():
    app_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "app.py")
    assert os.path.exists(app_path)
    # Compiles without syntax errors
    py_compile.compile(app_path, doraise=True)


def test_app_contains_expert_system_ui_elements():
    """Verify that app.py includes certainty meters, badges, and limitation warnings."""
    app_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "app.py")
    with open(app_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "Inference Certainty Factor (CF)" in content
    assert "Deterministic Physical Finding" in content
    assert "Conditional Diagnostic Hypothesis" in content
    assert "Domain Limitation Warning" in content
    assert "Differential Diagnoses / Competing Hypotheses" in content


def test_post_triage_audit_button_mode_switch():
    """Verify that clicking Launch Full Subsystem Audit switches selected_mode without widget errors."""
    from streamlit.testing.v1 import AppTest
    app_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "app.py")
    at = AppTest.from_file(app_path)
    at.run()
    assert not at.exception

    # Simulate a concluded emergency triage session
    at.session_state.emergency_history = [
        ("q_emergency_triage", "memory"),
        ("q_post_beeps", "no_beeps_normal"),
        ("q_ram_recognized", "full_ram_ok"),
        ("q_random_freezing", "no_freezing"),
    ]
    at.run()
    assert not at.exception

    # Locate and click the Launch Full 50-Point Subsystem Audit button
    target_btn = None
    for b in at.button:
        if "Launch Full 50-Point Subsystem Audit" in b.label:
            target_btn = b
            break

    assert target_btn is not None
    target_btn.click()
    at.run()

    # Must not raise StreamlitWidgetAlreadyInstantiatedError or any other exception
    assert not at.exception
    assert at.session_state.selected_mode == "🔍 Cascading Decision-Tree Audit"


