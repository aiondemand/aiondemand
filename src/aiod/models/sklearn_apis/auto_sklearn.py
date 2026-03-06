"""Auto-sklearn classifier."""

from aiod.models.apis import _ModelPkgSklearnEstimator


class AiodPkg__AutoSklearn(_ModelPkgSklearnEstimator):
    _tags = {
        "pkg_id": "__multiple",
        "python_dependencies": "auto-sklearn",
        "pkg_pypi_name": "autosklearn",
        "object_types": ["classifier", "regressor"],
    }

    _obj_dict = {
        "AutoSklearnClassifier": "autosklearn.classification.AutoSklearnClassifier",
        "AutoSklearnRegressor": "autosklearn.regression.AutoSklearnRegressor",
    }
    _type_of_objs = {
        "AutoSklearnClassifier": "classifier",
        "AutoSklearnRegressor": "regressor",
    }
    _objs_by_type = {
        "classifier": ["AutoSklearnClassifier"],
        "regressor": ["AutoSklearnRegressor"],
    }
