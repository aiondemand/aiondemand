# ruff: noqa: E501
"""LightGBM model package."""

from aiod.models.apis import _ModelPkgSklearnEstimator


class AiodPkg__LightGBM(_ModelPkgSklearnEstimator):
    _tags = {
        "pkg_id": "__multiple",
        "python_dependencies": "lightgbm",
        "pkg_pypi_name": "lightgbm",
        "object_types": ["classifier", "regressor"],
    }

    _obj_dict = {
        "DaskLGBMClassifier": "lightgbm.dask.DaskLGBMClassifier",
        "DaskLGBMRegressor": "lightgbm.dask.DaskLGBMRegressor",
        "LGBMClassifier": "lightgbm.sklearn.LGBMClassifier",
        "LGBMRegressor": "lightgbm.sklearn.LGBMRegressor",
    }

    _type_of_objs = {
        "DaskLGBMClassifier": "classifier",
        "DaskLGBMRegressor": "regressor",
        "LGBMClassifier": "classifier",
        "LGBMRegressor": "regressor",
    }

    _objs_by_type = {
        "classifier": [
            "DaskLGBMClassifier",
            "LGBMClassifier",
        ],
        "regressor": [
            "DaskLGBMRegressor",
            "LGBMRegressor",
        ],
    }
