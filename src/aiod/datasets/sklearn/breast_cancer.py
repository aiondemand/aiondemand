"""Breast Cancer dataset loader."""

from sklearn.datasets import load_breast_cancer

from aiod.datasets.sklearn._base import BaseSklearnDataset


class BreastCancer(BaseSklearnDataset):
    """Breast Cancer dataset loader.

    Examples
    --------
    >>> from aiod.datasets.sklearn import BreastCancer
    >>> dataset = BreastCancer()
    >>> X, y = dataset.load()
    >>> X = dataset.load("X")
    >>> y = dataset.load("y")
    """

    loader_func = load_breast_cancer

    _tags = {
        "name": "breast_cancer",
        "scitype": ["dataset", "dataset_tabular_classification"],
    }
