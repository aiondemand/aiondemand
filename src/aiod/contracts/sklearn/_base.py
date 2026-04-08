"""Base class for scikit-learn API contracts."""

from typing import Any

from aiod.contracts.base import _BaseContract
from aiod.contracts.utils import ContractError


class _BaseSklearnContract(_BaseContract):
    _tags = {
        "python_dependencies": "scikit-learn",
        "pkg_pypi_name": "scikit-learn",
        "scitype_name": "sklearn",
        "short_descr": "basic scitype for all scikit-learn contracts",
    }

    @classmethod
    def _resolve(cls, obj: Any) -> Any:
        """Resolve identifier to class."""
        obj = super()._resolve(obj)

        from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
        from sklearn.pipeline import Pipeline

        if isinstance(obj, Pipeline):
            if not obj.steps:
                raise ContractError(f"Pipeline has not steps, obj.steps={obj.steps}")

            return cls._resolve(obj.steps[-1][1])

        if isinstance(obj, (GridSearchCV, RandomizedSearchCV)):
            if obj.estimator is None:
                raise ContractError(
                    f"{obj} has no estimator, obj.estimator={obj.estimator}"
                )

            return cls._resolve(obj.estimator)

        obj = obj if isinstance(obj, type) else type(obj)

        return obj

    @classmethod
    def _check_structure(cls, obj: type) -> bool:
        from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
        from sklearn.pipeline import Pipeline

        if issubclass(obj, (Pipeline, GridSearchCV, RandomizedSearchCV)):
            raise ContractError(
                f"found class {obj}, object should be passed here instead"
            )

        return True

    @classmethod
    def _run_behavioral_tests(cls, obj: type):
        from sklearn.utils.estimator_checks import check_estimator

        results = check_estimator(obj())
        return results


__all__ = ["_BaseSklearnContract"]
