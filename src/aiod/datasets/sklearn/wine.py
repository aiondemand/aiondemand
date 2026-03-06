"""Wine dataset loader."""

from sklearn.datasets import load_wine

from aiod.datasets.sklearn._base import BaseSklearnDataset


class Wine(BaseSklearnDataset):
    """Wine dataset loader.

    Examples
    --------
    >>> from aiod.datasets.sklearn import Wine
    >>> dataset = Wine()
    >>> X, y = dataset.load()
    >>> X = dataset.load("X")
    >>> y = dataset.load("y")
    """

    loader_func = load_wine

    _tags = {
        "name": "wine",
        "scitype": ["dataset", "dataset_tabular_classification"],
    }
