# ruff: noqa: N802
"""Tests for OpenML dataset dispatch via aiod.get()."""

import pytest
from skbase.utils.dependencies import _check_soft_dependencies


@pytest.mark.skipif(
    not _check_soft_dependencies("openml", severity="none"),
    reason="openml-python not installed",
)
@pytest.mark.parametrize("identifier", [31, "credit-g"])
def test_get_openml(identifier):
    """aiod.get('openml://...') returns a valid OpenMLDataset."""
    import openml

    from aiod import get

    ds = get(f"openml://{identifier}")

    assert isinstance(ds, openml.OpenMLDataset)
