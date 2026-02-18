from aiod.models.apis import _ModelPkgClassifier


class AiodPkg__CatBoost(_ModelPkgClassifier):
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
        'CatboostError': '_catboost.CatboostError',
        'EFeaturesSelectionAlgorithm': 'catboost.core.EFeaturesSelectionAlgorithm',
        'EFeaturesSelectionGrouping': 'catboost.core.EFeaturesSelectionGrouping',
        'EFstrType': 'catboost.core.EFstrType',
        'EShapCalcType': 'catboost.core.EShapCalcType',
        'FeaturesData': '_catboost.FeaturesData',
        'MultiRegressionCustomMetric': '_catboost.MultiRegressionCustomMetric',
        'MultiRegressionCustomObjective': '_catboost.MultiRegressionCustomObjective',
        'MultiTargetCustomMetric': '_catboost.MultiTargetCustomMetric',
        'MultiTargetCustomObjective': '_catboost.MultiTargetCustomObjective',
        'Pool': 'catboost.core.Pool',
        'cv': 'catboost.core.cv',
        'sample_gaussian_process': 'catboost.core.sample_gaussian_process',
        'sum_models': 'catboost.core.sum_models',
        'to_classifier': 'catboost.core.to_classifier',
        'to_ranker': 'catboost.core.to_ranker',
        'to_regressor': 'catboost.core.to_regressor',
        'train': 'catboost.core.train'
    }