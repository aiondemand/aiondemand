# ruff: noqa: N802, E402
"""Tests for OpenML dataset loaders."""

import pytest

openml = pytest.importorskip("openml")

from aiod.data import OpenMLDataset


@pytest.fixture
def dataset():
    return OpenMLDataset(dataset_id=31)


def test_load_returns_X_y(dataset):
    """load() should return X, y."""
    X, y = dataset.load()

    assert X is not None
    assert y is not None
    assert len(X) == len(y)


def test_load_single_key(dataset):
    """load('X') and load('y') should return individual objects."""
    X = dataset.load("X")
    y = dataset.load("y")

    assert X is not None
    assert y is not None
    assert len(X) == len(y)


def test_load_multiple_args(dataset):
    """load('X','y') should return tuple in order."""
    X, y = dataset.load("X", "y")

    assert isinstance((X, y), tuple)
    assert len(X) == len(y)


def test_invalid_key_raises(dataset):
    """Invalid key should raise ValueError."""
    with pytest.raises(ValueError):
        dataset.load("invalid_key")


def test_keys_method(dataset):
    """keys() should list available dataset components."""
    keys = dataset.keys()

    assert "X" in keys
    assert "y" in keys
    assert len(keys) == 2


def test_explicit_target():
    """Explicit target parameter should work."""
    ds = OpenMLDataset(dataset_id=31, target="class")
    X, y = ds.load()

    assert X is not None
    assert y is not None
    assert len(X) == len(y)


def test_data_matches_openml_directly():
    """Dataset wrapper should match raw openml output."""
    import openml

    ds = OpenMLDataset(dataset_id=31)
    X1, y1 = ds.load()

    raw = openml.datasets.get_dataset(31)
    X2, y2, _, _ = raw.get_data(target=raw.default_target_attribute)

    assert X1.shape == X2.shape
    assert y1.shape == y2.shape


def test_get_openml_instance():
    """aiod.get('openml:31') should return an OpenMLDataset."""
    from aiod import get

    ds = get("openml:31")

    assert isinstance(ds, OpenMLDataset)
    assert ds.dataset_id == 31

    X, y = ds.load()
    assert X is not None
    assert y is not None


def test_get_openml_invalid_id():
    """aiod.get('openml:not_a_number') should raise ValueError."""
    from aiod import get

    with pytest.raises(ValueError, match="integer"):
        get("openml:not_a_number")
