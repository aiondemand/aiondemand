"""Adapters for scikit-learn cv splitters."""

from aiod.models.apis import _ModelPkgSklearnEstimator


class AiodPkg__SklearnCV(_ModelPkgSklearnEstimator):
    _tags = {
        "pkg_id": "__multiple",
        "python_dependencies": "scikit-learn",
        "pkg_pypi_name": "scikit-learn",
        "object_types": ["cross_validator"],
    }

    _obj_dict = {
        "KFold": "sklearn.model_selection.KFold",
        "StratifiedKFold": "sklearn.model_selection.StratifiedKFold",
    }

    _type_of_objs = {
        "KFold": "cross_validator",
        "StratifiedKFold": "cross_validator",
    }

    _objs_by_type = {
        "cross_validator": ["KFold", "StratifiedKFold"],
    }