"""Catboost Estimators."""

from aiod.models.apis import _ModelPkgSklearnEstimator


class AiodPkg__Catboost(_ModelPkgSklearnEstimator):
    _tags = {
        "pkg_id": "__multiple",
        "python_dependencies": "catboost",
        "pkg_pypi_name": "catboost",
        "object_types": [],  # needs update
    }
