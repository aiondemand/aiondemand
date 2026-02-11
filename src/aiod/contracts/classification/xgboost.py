"""XGBoost API contracts."""

from __future__ import annotations
from typing import Type
from aiod.contracts.base import BaseAPIContract


class XGBoostClassifierContract(BaseAPIContract):
    """Contract for XGBoost classifiers."""

    _tags = {
        "contract_type": "xgboost_classifier",
        "python_dependencies": "xgboost",
        "pkg_id": "XGBoostClassifierContract",
    }

    @classmethod
    def _check_structure(cls, obj: Type) -> bool:
        from xgboost import XGBClassifier

        if not issubclass(obj, XGBClassifier):
            raise TypeError("Object is not an XGBClassifier")

        for method in ["fit", "predict", "predict_proba"]:
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
        probs = instance.predict_proba(X)

        if len(preds) != len(y):
            raise RuntimeError("Predict output length mismatch")
        if probs.shape[0] != len(y):
            raise RuntimeError("Predict_proba output length mismatch")
