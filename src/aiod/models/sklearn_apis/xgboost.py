"""Xgboost classifier."""

from aiod.models.apis import _ModelPkgSklearnEstimator


class AiodPkg__XGBClassifier(_ModelPkgSklearnEstimator):
    _tags = {
        "pkg_id": "XGBClassifier",
        "python_dependencies": "xgboost",
        "pkg_pypi_name": "xgboost",
    }

    _obj = "xgboost.XGBClassifier"
