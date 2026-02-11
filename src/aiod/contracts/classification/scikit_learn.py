"""Sklearn API contracts."""

from __future__ import annotations

from typing import Type

from aiod.contracts.base import BaseAPIContract


class SklearnClassifierContract(BaseAPIContract):
    """Contract for sklearn-compatible classifiers."""

    _tags = {
        "contract_type": "sklearn_classifier",
        "python_dependencies": "scikit-learn",
        "pkg_id": "SklearnClassifierContract",
    }

    @classmethod
    def _check_structure(cls, obj: Type) -> bool:
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
    def _run_behavioral_tests(cls, obj: Type):
        import numpy as np

        X = np.array([[0, 0], [1, 1], [0, 1], [1, 0]])
        y = np.array([0, 1, 0, 1])

        instance = obj()
        instance.fit(X, y)
        preds = instance.predict(X)

        if len(preds) != len(y):
            raise RuntimeError("Predict output length mismatch")
