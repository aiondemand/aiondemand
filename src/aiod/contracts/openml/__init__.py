"""OpenML API contracts."""

from aiod.contracts.openml.contracts import (
    openml_classification_dataset,
    openml_dataset,
    openml_regression_dataset,
)

__all__ = [
    "openml_dataset",
    "openml_regression_dataset",
    "openml_classification_dataset",
]
