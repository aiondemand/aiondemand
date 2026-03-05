"""Iris dataset loader."""

from sklearn.datasets import load_iris

from aiod.datasets.sklearn._base import BaseSklearnDataset


class Iris(BaseSklearnDataset):
    loader_func = load_iris

    _tags = {
        "name": "iris",
        "scitype": "tabular_classification",
    }
