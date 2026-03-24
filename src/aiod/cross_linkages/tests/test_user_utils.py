"""Test utils for cross-linkages."""

import pytest

import aiod
import aiod.cross_linkages.cross_linkages as cross_linkages


@pytest.fixture
def fake_registry(monkeypatch):
    registry = {
        "10.1/test-doi": ["AlgoA", "AlgoB"],
        "10.2/test-doi": ["AlgoB"],
    }

    monkeypatch.setattr(cross_linkages, "PUB_ALGORITHM_REGISTRY", registry)
    return registry


@pytest.fixture
def fake_get(monkeypatch):
    def _fake_get(name):
        if name.endswith("()"):
            return f"instance:{name[:-2]}"
        return f"class:{name}"

    monkeypatch.setattr(cross_linkages, "get", _fake_get)


def test_get_from_pub_ids(fake_registry):
    result = aiod.get_from_pub("10.1/test-doi")
    assert result == ["AlgoA", "AlgoB"]


def test_get_from_pub_classes(fake_registry, fake_get):
    result = aiod.get_from_pub("10.1/test-doi", return_as="classes")
    assert result == ["class:AlgoA", "class:AlgoB"]


def test_get_from_pub_instances(fake_registry, fake_get):
    result = aiod.get_from_pub("10.1/test-doi", return_as="instances")
    assert result == ["instance:AlgoA", "instance:AlgoB"]


def test_get_from_pub_missing_doi(fake_registry):
    result = aiod.get_from_pub("10.999/unknown")
    assert result == []


def test_get_from_pub_invalid_mode(fake_registry):
    with pytest.raises(ValueError, match="Unknown return mode"):
        aiod.get_from_pub("10.1/test-doi", return_as="invalid")


def test_get_pubs_for_single_match(fake_registry):
    result = aiod.get_pubs_for("AlgoA")
    assert result == ["10.1/test-doi"]


def test_get_pubs_for_multiple_matches(fake_registry):
    result = aiod.get_pubs_for("AlgoB")
    assert sorted(result) == ["10.1/test-doi", "10.2/test-doi"]


def test_get_pubs_for_no_match(fake_registry):
    result = aiod.get_pubs_for("AlgoZ")
    assert result == []
