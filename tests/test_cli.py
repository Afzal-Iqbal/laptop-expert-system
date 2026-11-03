import subprocess
import sys
import os

def test_cli_audit_quick_execution():
    project_dir = os.path.dirname(os.path.dirname(__file__))
    cmd = [os.path.join(project_dir, ".venv", "bin", "python"), "cli.py", "--audit-quick"]
    result = subprocess.run(cmd, cwd=project_dir, capture_output=True, text=True)
    assert result.returncode == 0
    assert "50-POINT AUDIT SCORECARD COMPLETE" in result.stdout
    assert "Overall Health Score:" in result.stdout
    assert "100/100" in result.stdout
