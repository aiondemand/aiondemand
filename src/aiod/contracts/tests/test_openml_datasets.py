"""Test OpenML dataset contracts."""

import pytest
from skbase.utils.dependencies import _check_soft_dependencies, _safe_import

from aiod.contracts.openml import (
    openml_classification_dataset,
    openml_dataset,
    openml_regression_dataset,
)
from aiod.contracts.utils import ContractError

get_dataset = _safe_import(
    import_path="openml.datasets.get_dataset",
    pkg_name="openml",
)


@pytest.fixture
def iris():
    """OpenML iris dataset (classification)."""
    return get_dataset(61)


@pytest.fixture
def boston():
    """OpenML boston housing dataset (regression)."""
    return get_dataset(531)


@pytest.mark.skipif(
    not _check_soft_dependencies("openml", severity="none"),
    reason="run only if openml is installed",
)
@pytest.mark.parametrize(
    "dataset_fixture, contract, expected",
    [
        ("iris", openml_dataset, True),
        ("iris", openml_classification_dataset, True),
        ("iris", openml_regression_dataset, False),
        ("boston", openml_dataset, True),
        ("boston", openml_regression_dataset, True),
        ("boston", openml_classification_dataset, False),
    ],
)
def test_istypeof(request, dataset_fixture, contract, expected):
    dataset = request.getfixturevalue(dataset_fixture)

    if expected:
        assert contract.istypeof(dataset, raise_error=True) is True
    else:
        with pytest.raises(ContractError):
            contract.istypeof(dataset, raise_error=True)

        assert contract.istypeof(dataset) is False
