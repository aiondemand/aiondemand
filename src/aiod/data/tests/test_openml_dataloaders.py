# ruff: noqa: N802
"""Tests for OpenML dataset dispatch via aiod.get()."""

import pytest
from skbase.utils.dependencies import _check_soft_dependencies


@pytest.mark.skipif(
    not _check_soft_dependencies("openml", severity="none"),
    reason="openml-python not installed",
)
def test_get_openml_by_id():
    """aiod.get('openml://31') should return an OpenML dataset."""
    from aiod import get

    ds = get("openml://31")

    # Check it's a native OpenML dataset
    assert hasattr(ds, "get_data")
    assert hasattr(ds, "default_target_attribute")


@pytest.mark.skipif(
    not _check_soft_dependencies("openml", severity="none"),
    reason="openml-python not installed",
)
def test_get_openml_by_name():
    """aiod.get('openml://credit-g') should work with dataset name."""
    from aiod import get

    ds = get("openml://credit-g")

    assert hasattr(ds, "get_data")
