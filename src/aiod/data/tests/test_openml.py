# ruff: noqa: N802
"""Tests for OpenML dataset loading."""

import pytest
from skbase.utils.dependencies import _check_soft_dependencies


@pytest.mark.skipif(
    not _check_soft_dependencies("openml", severity="none"),
    reason="openml-python not installed",
)
@pytest.mark.parametrize("identifier", [31, "credit-g"])
def test_get_openml_dataset(identifier):
    """_get_openml_dataset returns a valid OpenMLDataset."""
    import openml

    from aiod.data._openml import _get_openml_dataset

    ds = _get_openml_dataset(identifier)

    assert isinstance(ds, openml.OpenMLDataset)
