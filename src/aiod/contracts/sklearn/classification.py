"""Scikit-learn classification API contract."""

from aiod.contracts.sklearn._base import _BaseSklearnContract


class classifier(_BaseSklearnContract):  # noqa: N801
    _tags = {
        "scitype_name": "classifier",
        "short_descr": "scitype for scikit-learn classification contract",
        "parent_scitype": "sklearn",
    }

    @classmethod
    def _deeper_check(cls, obj: type) -> bool:
        from sklearn.base import ClassifierMixin

        is_cls = isinstance(obj, type)

        if is_cls and issubclass(obj, ClassifierMixin):
            return True

        if not is_cls and isinstance(obj, ClassifierMixin):
            return True

        return False


"""
conditions for a classifier
(
    ( is_cls and issubclass(obj, ClassifierMixin) )
    or
    ( not is_cls and isinstance(obj, ClassifierMixin) )
)
and
super().check_estimator

"""
