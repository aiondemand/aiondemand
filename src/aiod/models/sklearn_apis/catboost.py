from aiod.models.apis import _ModelPkgSklearnEstimator


class AiodPkg__CatBoost(_ModelPkgSklearnEstimator):
    _tags = {
        "pkg_id": "__multiple",
        "python_dependencies": "catboost",
        "pkg_pypi_name": "catboost",
    }

    _obj_dict = {
        'CatBoost': 'catboost.core.CatBoost',
        'CatBoostClassifier': 'catboost.core.CatBoostClassifier',
        'CatBoostRanker': 'catboost.core.CatBoostRanker',
        'CatBoostRegressor': 'catboost.core.CatBoostRegressor',
    }
    
    _type_of_objs = {
        "CatBoost": ["classifier", "regressor"],
        "CatBoostClassifier": "classifier",
        "CatBoostRanker": "ranker",
        "CatBoostRegressor": "regressor",
    }

    _objs_by_type = {
        "classifier": [
            "CatBoost",
            "CatBoostClassifier",
        ],
        "regressor": [
            "CatBoost",
            "CatBoostRegressor",
        ],
        "ranker": [
            "CatBoostRanker",
        ],
    }