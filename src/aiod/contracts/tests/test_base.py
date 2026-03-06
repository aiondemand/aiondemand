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


@pytest.fixture
def contract():
    return DummyContract


def _generate_cases(obj, *args):
    return [
        (obj, *args),
        (obj(), *args),
        (obj.__name__, *args),
        (obj.__name__ + "()", *args),
    ]


@pytest.mark.parametrize(
    "obj,expected",
    [
        *_generate_cases(ValidEstimator, True),
        *_generate_cases(MissingPredict, False),
        *_generate_cases(BrokenBehavior, True),
        ("UnknownEstimator", False),
        ("UnknownEstimator()", False),
    ],
)
def test_istypeof(obj, contract, expected, mock_aiod_get):
    assert contract.istypeof(obj) is expected


@pytest.mark.parametrize(
    "obj,passed,errors",
    [
        *_generate_cases(ValidEstimator, True, None),
        *_generate_cases(MissingPredict, False, "Missing required method"),
        *_generate_cases(BrokenBehavior, False, "behavior failure"),
        ("UnknownEstimator", False, ""),
        ("UnknownEstimator()", False, ""),
    ],
)
def test_runtests(obj, contract, passed, errors, mock_aiod_get):
    result = contract.runtests(obj)
    assert result["passed"] is passed
    if passed:
        assert result["errors"] == []
    else:
        assert any(errors in e for e in result["errors"])
