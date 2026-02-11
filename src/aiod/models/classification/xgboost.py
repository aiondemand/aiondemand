"""Xgboost classifier."""

from aiod.models.apis import _ModelPkgClassifier


class AiodPkg__XGBClassifier(_ModelPkgClassifier):
    _tags = {
        "pkg_id": "XGBClassifier",
        "python_dependencies": "xgboost",
        "pkg_pypi_name": "xgboost",
    }

    _obj = "xgboost.XGBClassifier"
