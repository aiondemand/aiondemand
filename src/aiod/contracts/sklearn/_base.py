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
        # True: only after making sure there was no problem with obj
        # to comply with scikit-learn
        # False: if any problem is detected

        from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
        from sklearn.pipeline import Pipeline

        is_cls = isinstance(obj, type)

        if is_cls and issubclass(obj, (Pipeline, GridSearchCV, RandomizedSearchCV)):
            return False

        if isinstance(obj, Pipeline):
            if not obj.steps:
                return False
            return cls._check_structure(obj.steps[-1][1])

        if isinstance(obj, (GridSearchCV, RandomizedSearchCV)):
            if obj.estimator is None:
                return False
            return cls._check_structure(obj.estimator)

        return cls._deeper_check(obj)

    @classmethod
    def _deeper_check(cls, obj: type) -> bool:
        raise RuntimeError("abstract method")

    @classmethod
    def _run_behavioral_tests(cls, obj: type):
        from sklearn.utils.estimator_checks import check_estimator

        results = check_estimator(obj())
        return results


__all__ = ["_BaseSklearnContract"]
