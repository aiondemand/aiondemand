"""Tests for _AiodModelPkg materialization."""

import pytest

from aiod.models.base._base import _AiodModelPkg


class DummyCodePkg(_AiodModelPkg):
    _tags = {
        "pkg_id": "dummy_code_pkg",
        "pkg_obj": "code",
    }
    _obj = "obj = {'status': 'ok'}"


def test_materialize_code_exec_uses_explicit_namespace():
    """Test that code-based materialization returns the executed obj."""
    pkg = DummyCodePkg()
    result = pkg._materialize()

    assert result == {"status": "ok"}


class DummyMissingObjPkg(_AiodModelPkg):
    _tags = {
        "pkg_id": "dummy_missing_obj_pkg",
        "pkg_obj": "code",
    }
    _obj = "x = 10"


def test_materialize_code_raises_if_obj_not_defined():
    """Test that code-based materialization raises when obj is missing."""
    pkg = DummyMissingObjPkg()

    with pytest.raises(ValueError, match="did not define 'obj'"):
        pkg._materialize()