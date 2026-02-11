"""Auto-sklearn API contracts."""

from __future__ import annotations
from typing import Type
from aiod.contracts.base import BaseAPIContract


class AutoSklearnClassifierContract(BaseAPIContract):
    """Contract for auto-sklearn classifiers."""

    _tags = {
        "contract_type": "auto_sklearn_classifier",
        "python_dependencies": "auto-sklearn",
        "pkg_id": "AutoSklearnClassifierContract",
    }

    @classmethod
    def _check_structure(cls, obj: Type) -> bool:
        from autosklearn.classification import AutoSklearnClassifier
        from sklearn.base import BaseEstimator, ClassifierMixin

        if not issubclass(obj, (BaseEstimator, AutoSklearnClassifier)):
            raise TypeError("Object is not an AutoSklearnClassifier or BaseEstimator")

        for method in ["fit", "predict", "predict_proba"]:
            if not hasattr(obj, method):
                raise TypeError(f"Missing required method: {method}")

        return True

    @classmethod
    def _run_behavioral_tests(cls, obj: Type):
        import numpy as np

        X = np.array([[0, 0], [1, 1], [0, 1], [1, 0]])
        y = np.array([0, 1, 0, 1])

        instance = obj(time_left_for_this_task=30)
        instance.fit(X, y)
        preds = instance.predict(X)
        probs = instance.predict_proba(X)

        if len(preds) != len(y):
            raise RuntimeError("Predict output length mismatch")
        if probs.shape[0] != len(y):
            raise RuntimeError("Predict_proba output length mismatch")
