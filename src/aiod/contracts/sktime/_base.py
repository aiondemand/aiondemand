"""Base class for sktime API contracts."""

from aiod.contracts.base import _BaseContract


class _BaseSktimeContract(_BaseContract):
    _tags = {
        "python_dependencies": "sktime",
        "pkg_pypi_name": "sktime",
        "scitype_name": "sktime",
        "short_descr": "basic scitype for all sktime contracts",
    }

    @classmethod
    def _check_structure(cls, obj: type) -> bool:
        from sktime.base import BaseObject

        if not issubclass(obj, BaseObject):
            raise TypeError("Object is not a sktime BaseObject")

        return True

    @classmethod
    def _run_behavioral_tests(cls, obj: type):
        from sktime.utils.estimator_checks import check_estimator

        # sktime's check_estimator usually takes the class directly or an instance
        results = check_estimator(obj, return_exceptions=False)
        return results


__all__ = ["_BaseSktimeContract"]
