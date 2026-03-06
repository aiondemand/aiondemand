"""sklearn dataset loaders."""

from aiod.datasets.sklearn._base import BaseSklearnDataset
from aiod.datasets.sklearn.breast_cancer import BreastCancer
from aiod.datasets.sklearn.diabetes import Diabetes
from aiod.datasets.sklearn.digits import Digits
from aiod.datasets.sklearn.iris import Iris
from aiod.datasets.sklearn.linnerud import Linnerud
from aiod.datasets.sklearn.wine import Wine

__all__ = [
    "BaseSklearnDataset",
    "Iris",
    "Digits",
    "Diabetes",
    "Linnerud",
    "Wine",
    "BreastCancer",
]
