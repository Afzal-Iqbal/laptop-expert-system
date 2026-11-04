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

