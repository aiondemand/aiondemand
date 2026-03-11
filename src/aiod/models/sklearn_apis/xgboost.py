"""Xgboost classifier."""

from aiod.models.apis import _ModelPkgSklearnEstimator


class AiodPkg__XGB(_ModelPkgSklearnEstimator):
    _CLASSES_TO_IGNORE = ["XGBModel"]  # core model
    _tags = {
        "pkg_id": "__multiple",
        "python_dependencies": "xgboost",
        "pkg_pypi_name": "xgboost",
        "object_types": ["classifier", "regressor", "ranker"],
    }

    _obj_dict = {
        "DaskXGBClassifier": "xgboost.dask.DaskXGBClassifier",
        "DaskXGBRFClassifier": "xgboost.dask.DaskXGBRFClassifier",
        "DaskXGBRFRegressor": "xgboost.dask.DaskXGBRFRegressor",
        "DaskXGBRanker": "xgboost.dask.DaskXGBRanker",
        "DaskXGBRegressor": "xgboost.dask.DaskXGBRegressor",
        "XGBClassifier": "xgboost.sklearn.XGBClassifier",
        "XGBRanker": "xgboost.sklearn.XGBRanker",
        "XGBRFClassifier": "xgboost.sklearn.XGBRFClassifier",
        "XGBRFRegressor": "xgboost.sklearn.XGBRFRegressor",
        "XGBRegressor": "xgboost.sklearn.XGBRegressor",
    }

    _type_of_objs = {
        "DaskXGBClassifier": "classifier",
        "DaskXGBRFClassifier": "classifier",
        "DaskXGBRFRegressor": "regressor",
        "DaskXGBRanker": "ranker",
        "DaskXGBRegressor": "regressor",
        "XGBClassifier": "classifier",
        "XGBRanker": "ranker",
        "XGBRFClassifier": "classifier",
        "XGBRFRegressor": "regressor",
        "XGBRegressor": "regressor",
    }

    _objs_by_type = {
        "classifier": [
            "DaskXGBClassifier",
            "DaskXGBRFClassifier",
            "XGBClassifier",
            "XGBRFClassifier",
        ],
        "regressor": [
            "DaskXGBRFRegressor",
            "DaskXGBRegressor",
            "XGBRFRegressor",
            "XGBRegressor",
        ],
        "ranker": [
            "DaskXGBRanker",
            "XGBRanker",
        ],
    }
