import py_compile
import os

def test_app_syntax_and_compilation():
    app_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "app.py")
    assert os.path.exists(app_path)
    # Compiles without syntax errors
    py_compile.compile(app_path, doraise=True)
