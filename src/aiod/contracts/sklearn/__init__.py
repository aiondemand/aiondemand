"""Base class for scikit-learn API contracts."""

from aiod.contracts.sklearn.contracts import classifier, estimator

__all__ = [
    "estimator",
    "classifier",
]
