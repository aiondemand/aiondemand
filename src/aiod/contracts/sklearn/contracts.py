"""Scikit-learn API contracts."""

from aiod.contracts.sklearn._base import _BaseSklearnContract
from aiod.contracts.utils import ContractError


class estimator(_BaseSklearnContract):  # noqa: N801
    _tags = {
        "scitype_name": "estimator",
        "short_descr": "scitype for scikit-learn estimator contract",
        "parent_scitype": "sklearn",
    }

    @classmethod
    def _check_structure(cls, obj: type) -> bool:
        from sklearn.base import BaseEstimator

        if not issubclass(obj, BaseEstimator):
            raise ContractError(f"{obj} is not a subclass of BaseEstimator")

        return True


class regressor(_BaseSklearnContract):  # noqa: N801
    _tags = {
        "scitype_name": "regressor",
        "short_descr": "scitype for scikit-learn regressor contract",
        "parent_scitype": "sklearn",
    }

    @classmethod
    def _check_structure(cls, obj: type) -> bool:
        from sklearn.base import RegressorMixin

        super()._check_structure(obj)

        if not issubclass(obj, RegressorMixin):
            raise ContractError(f"{obj} is not a subclass of RegressorMixin")

        return True


class classifier(_BaseSklearnContract):  # noqa: N801
    _tags = {
        "scitype_name": "classifier",
        "short_descr": "scitype for scikit-learn classifier contract",
        "parent_scitype": "sklearn",
    }

    @classmethod
    def _check_structure(cls, obj: type) -> bool:
        from sklearn.base import ClassifierMixin

        super()._check_structure(obj)

        if not issubclass(obj, ClassifierMixin):
            raise ContractError(f"{obj} is not a subclass of ClassifierMixin")

        return True


class transformer(_BaseSklearnContract):  # noqa: N801
    _tags = {
        "scitype_name": "transformer",
        "short_descr": "scitype for scikit-learn transformer contract",
        "parent_scitype": "sklearn",
    }

    @classmethod
    def _check_structure(cls, obj: type) -> bool:
        from sklearn.base import TransformerMixin

        super()._check_structure(obj)

        if not issubclass(obj, TransformerMixin):
            raise ContractError(f"{obj} is not a subclass of TransformerMixin")

        return True


class clusterer(_BaseSklearnContract):  # noqa: N801
    _tags = {
        "scitype_name": "clusterer",
        "short_descr": "scitype for scikit-learn clusterer contract",
        "parent_scitype": "sklearn",
    }

    @classmethod
    def _check_structure(cls, obj: type) -> bool:
        from sklearn.base import ClusterMixin

        super()._check_structure(obj)

        if not issubclass(obj, ClusterMixin):
            raise ContractError(f"{obj} is not a subclass of ClusterMixin")

        return True


class biclusterer(_BaseSklearnContract):  # noqa: N801
    _tags = {
        "scitype_name": "biclusterer",
        "short_descr": "scitype for scikit-learn biclusterer contract",
        "parent_scitype": "sklearn",
    }

    @classmethod
    def _check_structure(cls, obj: type) -> bool:
        from sklearn.base import BiclusterMixin

        super()._check_structure(obj)

        if not issubclass(obj, BiclusterMixin):
            raise ContractError(f"{obj} is not a subclass of BiclusterMixin")

        return True


class density(_BaseSklearnContract):  # noqa: N801
    _tags = {
        "scitype_name": "density",
        "short_descr": "scitype for scikit-learn density contract",
        "parent_scitype": "sklearn",
    }

    @classmethod
    def _check_structure(cls, obj: type) -> bool:
        from sklearn.base import DensityMixin

        super()._check_structure(obj)

        if not issubclass(obj, DensityMixin):
            raise ContractError(f"{obj} is not a subclass of DensityMixin")

        return True


class outlier_detector(_BaseSklearnContract):  # noqa: N801
    _tags = {
        "scitype_name": "outlier_detector",
        "short_descr": "scitype for scikit-learn outlier_detector contract",
        "parent_scitype": "sklearn",
    }

    @classmethod
    def _check_structure(cls, obj: type) -> bool:
        from sklearn.base import OutlierMixin

        super()._check_structure(obj)

        if not issubclass(obj, OutlierMixin):
            raise ContractError(f"{obj} is not a subclass of OutlierMixin")

        return True


__all__ = [
    "estimator",
    "regressor",
    "classifier",
    "transformer",
    "clusterer",
    "biclusterer",
    "density",
    "outlier_detector",
]
