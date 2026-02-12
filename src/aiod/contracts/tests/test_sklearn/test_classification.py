import pytest
import aiod
from aiod.contracts import SklearnClassifierContract

from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.ensemble import RandomForestClassifier


class NotEstimator:
    pass


class MissingFit(BaseEstimator, ClassifierMixin):
    def predict(self, X):
        return [0] * len(X)


class BrokenBehaviorClassifier(RandomForestClassifier):
    def predict(self, X):
        raise RuntimeError("behavior failure")


@pytest.fixture
def contract():
    return SklearnClassifierContract


@pytest.fixture
def valid_class():
    return RandomForestClassifier


@pytest.fixture
def missing_fit_class():
    return MissingFit


@pytest.fixture
def not_estimator_class():
    return NotEstimator


@pytest.fixture
def broken_behavior_class():
    return BrokenBehaviorClassifier


@pytest.fixture
def mock_aiod_get(monkeypatch):
    def _mock_get(identifier: str):
        if identifier == "RandomForestClassifier":
            from sklearn.ensemble import RandomForestClassifier
            return RandomForestClassifier
        raise ValueError("not found")

    monkeypatch.setattr(aiod, "get", _mock_get)


def test_isinhabitant_with_class(contract, valid_class):
    assert contract.isinhabitant(valid_class) is True


def test_isinhabitant_with_string(contract, mock_aiod_get):
    assert contract.isinhabitant("RandomForestClassifier") is True


def test_isinhabitant_invalid_string(contract, mock_aiod_get):
    assert contract.isinhabitant("UnknownClassifier") is False


def test_isinhabitant_not_estimator(contract, not_estimator_class):
    assert contract.isinhabitant(not_estimator_class) is False


def test_runtests_success(contract, valid_class):
    result = contract.runtests(valid_class)
    assert result["passed"] is True
    assert result["errors"] == []


def test_runtests_structure_failure(contract, missing_fit_class):
    result = contract.runtests(missing_fit_class)
    assert result["passed"] is False
    assert any("Missing required method" in e for e in result["errors"])


def test_runtests_behavior_failure(contract, broken_behavior_class):
    result = contract.runtests(broken_behavior_class)
    assert result["passed"] is False
    assert any("behavior failure" in e for e in result["errors"])
