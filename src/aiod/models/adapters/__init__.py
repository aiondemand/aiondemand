"""Sklearn-compatible adapters for non-sklearn model libraries."""

from aiod.models.adapters._tabular_adapter import (
    _PyTorchTabularClassifierAdapter,
    _PyTorchTabularRegressorAdapter,
)

__all__ = [
    "_PyTorchTabularClassifierAdapter",
    "_PyTorchTabularRegressorAdapter",
]
