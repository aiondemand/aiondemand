from aiod.models.apis import _ModelPkgClassifier


class AiodPkg__LightGBM(_ModelPkgClassifier):
    _tags = {
        "pkg_id": "__multiple",
        "python_dependencies": "lightgbm",
        "pkg_pypi_name": "lightgbm",
    }

    _obj_dict = {
        'DaskLGBMClassifier': 'lightgbm.dask.DaskLGBMClassifier',
        'DaskLGBMRanker': 'lightgbm.dask.DaskLGBMRanker',
        'DaskLGBMRegressor': 'lightgbm.dask.DaskLGBMRegressor',
        'LGBMClassifier': 'lightgbm.sklearn.LGBMClassifier',
        'LGBMModel': 'lightgbm.sklearn.LGBMModel',
        'LGBMRanker': 'lightgbm.sklearn.LGBMRanker',
        'LGBMRegressor': 'lightgbm.sklearn.LGBMRegressor',
    }