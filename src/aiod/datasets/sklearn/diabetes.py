"""Diabetes dataset loader."""

from sklearn.datasets import load_diabetes

from aiod.datasets.sklearn._base import BaseSklearnDataset


class Diabetes(BaseSklearnDataset):
    """Diabetes dataset loader.

    Examples
    --------
    >>> from aiod.datasets.sklearn import Diabetes
    >>> dataset = Diabetes()
    >>> X, y = dataset.load()
    >>> X = dataset.load("X")
    >>> y = dataset.load("y")
    """

    loader_func = load_diabetes

    _tags = {
        "name": "diabetes",
        "scitype": ["dataset", "dataset_tabular_regression"],
    }
