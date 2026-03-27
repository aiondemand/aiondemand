"""Test cross-linkages with real RandomForestClassifier."""

import pytest
from sklearn.ensemble import RandomForestClassifier

import aiod
import aiod.cross_linkages.cross_linkages as cross_linkages


@pytest.fixture
def rf_registry(monkeypatch):
    registry = {
        "10.1/test-doi": ["RandomForestClassifier"],
    }
    monkeypatch.setattr(cross_linkages, "PUB_ALGORITHM_REGISTRY", registry)
    return registry


@pytest.fixture
def rf_get(monkeypatch):
    def _fake_get(name):
        if name == "RandomForestClassifier":
            return RandomForestClassifier
        raise ValueError(f"Unknown algorithm: {name}")

    monkeypatch.setattr(cross_linkages, "get", _fake_get)


def test_get_from_pub_ids(rf_registry):
    result = aiod.get_from_pub("10.1/test-doi")
    assert result == ["RandomForestClassifier"]


def test_get_from_pub_classes(rf_registry, rf_get):
    result = aiod.get_from_pub("10.1/test-doi", return_as="classes")
    assert result == [RandomForestClassifier]


def test_get_from_pub_instances(rf_registry, rf_get):
    result = aiod.get_from_pub("10.1/test-doi", return_as="instances")

    assert len(result) == 1
    assert isinstance(result[0], RandomForestClassifier)


def test_get_from_pub_missing_doi(rf_registry):
    result = aiod.get_from_pub("10.999/unknown")
    assert result == []


def test_get_from_pub_invalid_mode(rf_registry):
    with pytest.raises(ValueError, match="Unknown return mode"):
        aiod.get_from_pub("10.1/test-doi", return_as="invalid")


def test_get_pubs_for_match(rf_registry):
    result = aiod.get_pubs_for("RandomForestClassifier")
    assert result == ["10.1/test-doi"]


def test_get_pubs_for_no_match(rf_registry):
    result = aiod.get_pubs_for("AlgoX")
    assert result == []
