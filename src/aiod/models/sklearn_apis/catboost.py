from aiod.models.apis import _ModelPkgSklearnEstimator


class AiodPkg__CatBoost(_ModelPkgSklearnEstimator):
    _tags = {
        "pkg_id": "__multiple",
        "python_dependencies": "catboost",
        "pkg_pypi_name": "catboost",
        "object_types": ["classifier", "regressor"],
    }

    _obj_dict = {
        "CatBoostClassifier": "catboost.core.CatBoostClassifier",
        "CatBoostRegressor": "catboost.core.CatBoostRegressor",
    }

    _type_of_objs = {
        "CatBoostClassifier": "classifier",
        "CatBoostRegressor": "regressor",
    }

    _objs_by_type = {
        "classifier": [
            "CatBoostClassifier",
        ],
        "regressor": [
            "CatBoostRegressor",
        ],
    }
