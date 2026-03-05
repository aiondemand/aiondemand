"""sklearn dataset loaders."""

from aiod.datasets.sklearn._base import BaseSklearnDataset
from aiod.datasets.sklearn.iris import Iris

__all__ = ["BaseSklearnDataset", "Iris"]
