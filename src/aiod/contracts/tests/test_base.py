import pytest

import aiod
from aiod.contracts.base import _BaseContract


class ValidEstimator:
    def fit(self, X, y):  # noqa: N803
        return self

    def predict(self, X):  # noqa: N803
        return [0] * len(X)


class MissingPredict:
    def fit(self, X, y):  # noqa: N803
        return self


class BrokenBehavior:
    def fit(self, X, y):  # noqa: N803
        return self

    def predict(self, X):  # noqa: N803
        raise RuntimeError("behavior failure")


class DummyContract(_BaseContract):
    _tags = {
        "python_dependencies": None,
        "pkg_pypi_name": None,
        "scitype_name": "dummy",
        "short_descr": "basic scitype for all dummy DummyContract",
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
def mock_aiod_get(monkeypatch):
    def _mock_get(identifier: str):
        if identifier == "ValidEstimator":
            return ValidEstimator
        elif identifier == "ValidEstimator()":
            return ValidEstimator()
        elif identifier == "MissingPredict":
            return MissingPredict
        elif identifier == "MissingPredict()":
            return MissingPredict()
        elif identifier == "BrokenBehavior":
            return BrokenBehavior
        elif identifier == "BrokenBehavior()":
            return BrokenBehavior()
        raise ValueError("not found")

    monkeypatch.setattr(aiod, "get", _mock_get)


@pytest.mark.parametrize(
    "obj,expected",
    [
        (ValidEstimator, True),
        ("ValidEstimator", True),
        (ValidEstimator(), True),
        ("ValidEstimator()", True),
        (MissingPredict, False),
        ("MissingPredict", False),
        (MissingPredict(), False),
        ("MissingPredict()", False),
        (BrokenBehavior, True),
        ("BrokenBehavior", True),
        (BrokenBehavior(), True),
        ("BrokenBehavior()", True),
        ("UnknownEstimator", False),
        ("UnknownEstimator()", False),
    ],
)
def test_istypeof_with_class(mock_aiod_get, obj, expected):
    assert DummyContract.istypeof(obj) is expected


@pytest.mark.parametrize(
    "obj,passed,errors",
    [
        (ValidEstimator, True, None),
        (MissingPredict, False, "Missing required method"),
        (BrokenBehavior, False, "behavior failure"),
    ],
)
def test_runtests(obj, passed, errors):
    result = DummyContract.runtests(obj)
    assert result["passed"] is passed
    if errors is not None:
        assert any(errors in e for e in result["errors"])
