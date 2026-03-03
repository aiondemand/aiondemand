"""Scikit-learn classification API contract."""

from __future__ import annotations

from aiod.contracts.sklearn._base import _BaseSklearnContract


class classifier(_BaseSklearnContract):  # noqa: N801
    _tags = {
        "scitype_name": "classifier",
        "short_descr": "scitype for scikit-learn classification contract",
        "parent_scitype": "sklearn",
    }

    @classmethod
    def _check_structure(cls, obj: type) -> bool:
        from sklearn.base import ClassifierMixin

        super()._check_structure(obj)

        if not issubclass(obj, ClassifierMixin):
            raise TypeError("Object is not a sklearn ClassifierMixin")

        return True
