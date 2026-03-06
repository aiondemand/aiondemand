"""Iris dataset loader."""

from sklearn.datasets import load_iris

from aiod.datasets.sklearn._base import BaseSklearnDataset


class Iris(BaseSklearnDataset):
    """Iris dataset loader.

    Examples
    --------
    >>> from aiod.datasets.sklearn import Iris
    >>> dataset = Iris()
    >>> X, y = dataset.load()
    >>> X = dataset.load("X")
    >>> y = dataset.load("y")
    """

    loader_func = load_iris

    _tags = {
        "name": "iris",
        "scitype": ["dataset", "dataset_tabular_classification"],
    }
