"""Digits dataset loader."""

from sklearn.datasets import load_digits

from aiod.datasets.sklearn._base import BaseSklearnDataset


class Digits(BaseSklearnDataset):
    """Digits dataset loader.

    Examples
    --------
    >>> from aiod.datasets.sklearn import Digits
    >>> dataset = Digits()
    >>> X, y = dataset.load()
    >>> X = dataset.load("X")
    >>> y = dataset.load("y")
    """

    loader_func = load_digits

    _tags = {
        "name": "digits",
        "scitype": ["dataset", "dataset_tabular_classification"],
    }
