"""LightGBM Estimators."""

from aiod.models.apis import _ModelPkgSklearnEstimator


class AiodPkg__LightGBM(_ModelPkgSklearnEstimator):
    _CLASSES_TO_IGNORE = ["LGBMModel"]  # core model
    _tags = {
        "pkg_id": "__multiple",
        "python_dependencies": "lightgbm",
        "pkg_pypi_name": "lightgbm",
        "object_types": [],  # needs update
    }
