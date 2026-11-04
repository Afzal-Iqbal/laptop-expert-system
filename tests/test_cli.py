import subprocess
import sys
import os

def test_cli_audit_quick_execution():
    project_dir = os.path.dirname(os.path.dirname(__file__))
    cmd = [os.path.join(project_dir, ".venv", "bin", "python"), "cli.py", "--audit-quick"]
    result = subprocess.run(cmd, cwd=project_dir, capture_output=True, text=True)
    assert result.returncode == 0
    assert "CASCADING AUDIT SCORECARD COMPLETE" in result.stdout
    assert "Overall Health Score:" in result.stdout
    assert "100/100" in result.stdout


def test_cli_emergency_conditional_diagnosis():
    """Verify that emergency triage CLI outputs certainty factor and competing hypotheses."""
    project_dir = os.path.dirname(os.path.dirname(__file__))
    cmd = [os.path.join(project_dir, ".venv", "bin", "python"), "cli.py", "--emergency"]
    # Inputs: (1) power symptom -> (3) turns_on_then_dies
    input_str = "1\n3\n"
    result = subprocess.run(cmd, cwd=project_dir, input=input_str, capture_output=True, text=True)
    assert result.returncode == 0
    assert "DIAGNOSIS CONCLUDED: Motherboard Short Circuit" in result.stdout
    assert "Certainty Factor:    85% [CONDITIONAL (Heuristic Hypothesis)]" in result.stdout
    assert "Differential Diagnoses / Competing Hypotheses" in result.stdout
    assert "CPU/GPU Thermal Overheat Cutoff" in result.stdout


def test_cli_emergency_deterministic_diagnosis():
    """Verify that deterministic triage CLI outputs physical proof badge."""
    project_dir = os.path.dirname(os.path.dirname(__file__))
    cmd = [os.path.join(project_dir, ".venv", "bin", "python"), "cli.py", "--emergency"]
    # Inputs: (1) power symptom -> (2) turns_on_normal -> (3) instant_shutoff_unplug
    input_str = "1\n2\n3\n"
    result = subprocess.run(cmd, cwd=project_dir, input=input_str, capture_output=True, text=True)
    assert result.returncode == 0
    assert "DIAGNOSIS CONCLUDED: Dead Internal Battery Pack" in result.stdout
    assert "Certainty Factor:    95% [DETERMINISTIC (Physical Proof)]" in result.stdout


def test_cli_displays_prescribed_desk_test():
    """Verify that CLI formats and presents prescribed clinical desk tests with instructions."""
    project_dir = os.path.dirname(os.path.dirname(__file__))
    cmd = [os.path.join(project_dir, ".venv", "bin", "python"), "cli.py", "--emergency"]
    # Inputs: (2) display -> (2) screen_completely_dark -> (2) faint_image_seen
    input_str = "2\n2\n2\n"
    result = subprocess.run(cmd, cwd=project_dir, input=input_str, capture_output=True, text=True)
    assert result.returncode == 0
    assert "[DOCTOR'S PRESCRIBED TEST] Smartphone Flashlight Screen Test" in result.stdout
    assert "Instructions (Perform this safe desk test now):" in result.stdout
    assert "Doctor's Prescription & Actionable Treatment Plan:" in result.stdout
    assert "DIAGNOSIS CONCLUDED: Blown Screen Backlight Fuse" in result.stdout



