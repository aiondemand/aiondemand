# ruff: noqa: E501
"""LightGBM model package."""

from aiod.models.apis import _ModelPkgClassifier


class AiodPkg__LightGBM(_ModelPkgClassifier):
    _tags = {
        "pkg_id": "__multiple",
        "python_dependencies": "lightgbm",
        "pkg_pypi_name": "lightgbm",
        "object_types": ["classifier", "regressor", "ranker"],
    }

    _obj_dict = {
        "DaskLGBMClassifier": "lightgbm.dask.DaskLGBMClassifier",
        "DaskLGBMRanker": "lightgbm.dask.DaskLGBMRanker",
        "DaskLGBMRegressor": "lightgbm.dask.DaskLGBMRegressor",
        "LGBMClassifier": "lightgbm.sklearn.LGBMClassifier",
        "LGBMModel": "lightgbm.sklearn.LGBMModel",
        "LGBMRanker": "lightgbm.sklearn.LGBMRanker",
        "LGBMRegressor": "lightgbm.sklearn.LGBMRegressor",
    }

    _type_of_objs = {
        "DaskLGBMClassifier": "classifier",
        "DaskLGBMRanker": "ranker",
        "DaskLGBMRegressor": "regressor",
        "LGBMClassifier": "classifier",
        "LGBMModel": ["classifier", "regressor"],
        "LGBMRanker": "ranker",
        "LGBMRegressor": "regressor",
    }

    _objs_by_type = {
        "classifier": [
            "DaskLGBMClassifier",
            "LGBMClassifier",
            "LGBMModel",
        ],
        "regressor": [
            "DaskLGBMRegressor",
            "LGBMRegressor",
            "LGBMModel",
        ],
        "ranker": [
            "DaskLGBMRanker",
            "LGBMRanker",
        ],
    }
