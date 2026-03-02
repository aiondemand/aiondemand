import pytest
from skbase.utils.dependencies import _safe_import

import aiod
from aiod.contracts import SklearnClassificationContract

BaseEstimator = _safe_import(
    import_path="sklearn.base.BaseEstimator", pkg_name="scikit-learn"
)
ClassifierMixin = _safe_import(
    import_path="sklearn.base.ClassifierMixin", pkg_name="scikit-learn"
)
LogisticRegression = _safe_import(
    import_path="sklearn.linear_model.LogisticRegression", pkg_name="scikit-learn"
)


class NotEstimator:
    pass


class MissingFit(BaseEstimator, ClassifierMixin):
    def predict(self, X):  # noqa: N803
        return [0] * len(X)


class BrokenBehaviorClassifier(LogisticRegression):
    def predict(self, X):  # noqa: N803
        raise RuntimeError("behavior failure")


@pytest.fixture
def contract():
    return SklearnClassificationContract


@pytest.fixture
def valid_class():
    return LogisticRegression


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
        if identifier == "LogisticRegression":
            return LogisticRegression
        raise ValueError("not found")

    monkeypatch.setattr(aiod, "get", _mock_get)


def test_istypeof_with_class(contract, valid_class):
    assert contract.istypeof(valid_class) is True


def test_istypeof_with_string(contract, mock_aiod_get):
    assert contract.istypeof("LogisticRegression") is True


def test_istypeof_invalid_string(contract, mock_aiod_get):
    assert contract.istypeof("UnknownClassifier") is False


def test_istypeof_not_estimator(contract, not_estimator_class):
    assert contract.istypeof(not_estimator_class) is False


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
