"""Linnerud dataset loader."""

from sklearn.datasets import load_linnerud

from aiod.datasets.sklearn._base import BaseSklearnDataset


class Linnerud(BaseSklearnDataset):
    """Linnerud dataset loader.

    Examples
    --------
    >>> from aiod.datasets.sklearn import Linnerud
    >>> dataset = Linnerud()
    >>> X, y = dataset.load()
    >>> X = dataset.load("X")
    >>> y = dataset.load("y")
    """

    loader_func = load_linnerud

    _tags = {
        "name": "linnerud",
        "scitype": ["dataset", "dataset_tabular_regression"],
    }
