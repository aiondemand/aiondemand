"""API contract definitions."""

from aiod.contracts.base import BaseAPIContract
from aiod.contracts.sklearn import SklearnClassifierContract


__all__ = [
    "BaseAPIContract",
    "SklearnClassifierContract",
]
