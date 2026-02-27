"""Adapters for scikit-learn resamplers."""

from aiod.models.apis import _ModelPkgSklearnEstimator


class AiodPkg__SklearnResamplers(_ModelPkgSklearnEstimator):
    _tags = {
        "pkg_id": "__multiple",
        "python_dependencies": "scikit-learn",
        "pkg_pypi_name": "scikit-learn",
        "object_types": ["resampler"],
    }

    _obj_dict = {
        "KFold": "sklearn.model_selection.KFold",
        "StratifiedKFold": "sklearn.model_selection.StratifiedKFold",
    }

    _type_of_objs = {
        "KFold": "resampler",
        "StratifiedKFold": "resampler",
    }

    _objs_by_type = {
        "resampler": ["KFold", "StratifiedKFold"],
    }