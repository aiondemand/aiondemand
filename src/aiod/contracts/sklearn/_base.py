"""Base class for scikit-learn API contracts."""

from __future__ import annotations

from aiod.contracts.base import _BaseContract


class _BaseSklearnContract(_BaseContract):
    _tags = {
        "scitype_name": "sklearn_contract",
        "short_descr": "basic scitype for all scikit-learn contracts",
        "parent_scitype": "contract",
    }

    @classmethod
    def _check_structure(cls, obj: type) -> bool:
        from sklearn.base import BaseEstimator

        if not issubclass(obj, BaseEstimator):
            raise TypeError("Object is not a sklearn BaseEstimator")

        for method in ["fit", "predict"]:
            if not hasattr(obj, method):
                raise TypeError(f"Missing required method: {method}")

        return True

    @classmethod
    def _run_behavioral_tests(cls, obj: type):
        from sklearn.utils.estimator_checks import check_estimator

        results = check_estimator(obj())
        return results


__all__ = ["_BaseSklearnContract"]
