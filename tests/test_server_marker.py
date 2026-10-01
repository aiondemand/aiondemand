"""Contract tests for the ``server`` pytest marker setup.

The integration tests in ``tests/test_integration.py`` connect to a live AIoD
server, so they are deselected by default and must stay runnable via
``pytest -m server``. These tests guard that contract.

See https://github.com/aiondemand/aiondemand/issues/241
"""

import ast
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def _read_pyproject_text():
    return (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")


def _read_integration_module():
    return ast.parse(
        (REPO_ROOT / "tests" / "test_integration.py").read_text(encoding="utf-8")
    )


def test_server_marker_is_registered():
    """The server marker must stay registered, else -m server errors out."""
    assert "server: connects to an AIoD server" in _read_pyproject_text()


def test_default_addopts_deselect_server_tests():
    """Default runs must keep deselecting server tests (no live server hits)."""
    assert "addopts = \"-m 'not server'\"" in _read_pyproject_text()


def test_integration_tests_are_all_marked_server():
    """Every test in test_integration.py must carry the server mark.

    The module docstring promises these tests only run with
    ``pytest -m server``. An unmarked test would hit the live AIoD server
    during default and CI runs.
    """
    module = _read_integration_module()
    test_functions = [
        node
        for node in ast.walk(module)
        if isinstance(node, ast.FunctionDef) and node.name.startswith("test_")
    ]
    assert test_functions, "expected at least one test in test_integration.py"
    for func in test_functions:
        marks = [
            decorator.func.attr
            for decorator in func.decorator_list
            if isinstance(decorator, ast.Call)
            and isinstance(decorator.func, ast.Attribute)
            and isinstance(decorator.func.value, ast.Attribute)
            and decorator.func.value.attr == "mark"
        ]
        assert "server" in marks, f"{func.name} is missing @pytest.mark.server"


def test_integration_docstring_documents_how_to_run():
    """The module docstring must tell users how to run these tests.

    Regression test for #241: running ``pytest tests/test_integration.py``
    deselected everything with exit code 5 and nothing documented the
    ``-m server`` override.
    """
    docstring = ast.get_docstring(_read_integration_module()) or ""
    assert "-m server" in docstring
