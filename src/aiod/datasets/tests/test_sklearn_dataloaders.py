# ruff: noqa: N802
"""Tests for sklearn dataset loaders."""

import pytest
from sklearn.datasets import load_iris

from aiod.datasets.sklearn.iris import Iris


def test_load_returns_X_y():
    """load() should return X, y."""
    ds = Iris()

    X, y = ds.load()

    assert X is not None
    assert y is not None
    assert len(X) == len(y)


def test_load_single_key():
    """load('X') and load('y') should return individual objects."""
    ds = Iris()

    X = ds.load("X")
    y = ds.load("y")

    assert X is not None
    assert y is not None
    assert len(X) == len(y)


def test_getitem_interface():
    """Dataset should support dictionary-style access."""
    ds = Iris()

    X = ds["X"]
    y = ds["y"]

    assert len(X) == len(y)


def test_load_multiple_args():
    """load('X','y') should return tuple in order."""
    ds = Iris()

    X, y = ds.load("X", "y")

    assert isinstance((X, y), tuple)
    assert len(X) == len(y)


def test_invalid_key_raises():
    """Invalid key should raise ValueError."""
    ds = Iris()

    with pytest.raises(ValueError):
        ds.load("invalid_key")


def test_keys_method():
    """keys() should list available dataset components."""
    ds = Iris()

    keys = ds.keys()

    assert "X" in keys
    assert "y" in keys
    assert len(keys) == 2


def test_data_matches_sklearn():
    """Dataset wrapper should match sklearn loader output."""
    ds = Iris()

    X1, y1 = ds.load()
    X2, y2 = load_iris(return_X_y=True)

    assert X1.shape == X2.shape
    assert y1.shape == y2.shape
