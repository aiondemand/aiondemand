"""Base class for scikit-learn API contracts."""

from aiod.contracts.base import _BaseContract


class _BaseSklearnContract(_BaseContract):
    _tags = {
        "python_dependencies": "scikit-learn",
        "pkg_pypi_name": "scikit-learn",
        "scitype_name": "sklearn",
        "short_descr": "basic scitype for all scikit-learn contracts",
    }

    @classmethod
    def _check_structure(cls, obj: type) -> bool:
        from sklearn.base import BaseEstimator

        if not issubclass(obj, BaseEstimator):
            raise TypeError("Object is not a sklearn BaseEstimator")

        return True

    @classmethod
    def _run_behavioral_tests(cls, obj: type):
        from sklearn.utils.estimator_checks import check_estimator

        results = check_estimator(obj())
        return results


__all__ = ["_BaseSklearnContract"]
