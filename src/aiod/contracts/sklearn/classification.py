"""Sklearn API contracts."""

from __future__ import annotations

from aiod.contracts.base import _BaseContract


class SklearnClassifierContract(_BaseContract):
    """Contract for sklearn-compatible classifiers."""

    @classmethod
    def _check_structure(cls, obj: type) -> bool:
        from sklearn.base import BaseEstimator, ClassifierMixin

        if not issubclass(obj, BaseEstimator):
            raise TypeError("Object is not a sklearn BaseEstimator")

        if not issubclass(obj, ClassifierMixin):
            raise TypeError("Object is not a sklearn ClassifierMixin")

        for method in ["fit", "predict"]:
            if not hasattr(obj, method):
                raise TypeError(f"Missing required method: {method}")

        return True

    @classmethod
    def _run_behavioral_tests(cls, obj: type):
        import numpy as np

        X = np.array([[0, 0], [1, 1], [0, 1], [1, 0]])
        y = np.array([0, 1, 0, 1])

        instance = obj()
        instance.fit(X, y)
        preds = instance.predict(X)

        if len(preds) != len(y):
            raise RuntimeError("Predict output length mismatch")
