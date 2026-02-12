import pytest
import aiod

from aiod.contracts import BaseAPIContract


class ValidEstimator:
    def fit(self, X, y):
        return self

    def predict(self, X):
        return [0] * len(X)


class MissingPredict:
    def fit(self, X, y):
        return self


class BrokenBehavior:
    def fit(self, X, y):
        return self

    def predict(self, X):
        raise RuntimeError("behavior failure")


class DummyContract(BaseAPIContract):
    _tags = {
        "contract_type": "dummy",
        "python_dependencies": None,
        "pkg_id": "DummyContract",
    }

    @classmethod
    def _check_structure(cls, obj):
        obj_cls = obj if isinstance(obj, type) else type(obj)
        for method in ["fit", "predict"]:
            if not hasattr(obj_cls, method):
                raise TypeError(f"Missing required method: {method}")
        return True

    @classmethod
    def _run_behavioral_tests(cls, obj):
        instance = obj() if isinstance(obj, type) else obj
        instance.fit([[0]], [0])
        preds = instance.predict([[0]])

        if not isinstance(preds, list):
            raise RuntimeError("predict must return list")


@pytest.fixture
def contract():
    return DummyContract


@pytest.fixture
def valid_class():
    return ValidEstimator


@pytest.fixture
def missing_class():
    return MissingPredict


@pytest.fixture
def broken_class():
    return BrokenBehavior


@pytest.fixture
def mock_aiod_get(monkeypatch):
    def _mock_get(identifier: str):
        if identifier == "ValidEstimator":
            return ValidEstimator
        raise ValueError("not found")

    monkeypatch.setattr(aiod, "get", _mock_get)


def test_isinhabitant_with_class(contract, valid_class):
    assert contract.isinhabitant(valid_class) is True


def test_isinhabitant_with_string(contract, mock_aiod_get):
    assert contract.isinhabitant("ValidEstimator") is True


def test_isinhabitant_invalid_string(contract, mock_aiod_get):
    assert contract.isinhabitant("UnknownEstimator") is False


def test_runtests_success(contract, valid_class):
    result = contract.runtests(valid_class)
    assert result["passed"] is True
    assert result["errors"] == []


def test_runtests_structure_failure(contract, missing_class):
    result = contract.runtests(missing_class)
    assert result["passed"] is False
    assert any("Missing required method" in e for e in result["errors"])


def test_runtests_behavior_failure(contract, broken_class):
    result = contract.runtests(broken_class)
    assert result["passed"] is False
    assert any("behavior failure" in e for e in result["errors"])
