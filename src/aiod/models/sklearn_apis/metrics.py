"""Adapters for scikit-learn metrics."""

from aiod.models.apis import _ModelPkgSklearnEstimator


class AiodPkg__SklearnMetrics(_ModelPkgSklearnEstimator):
    _tags = {
        "pkg_id": "__multiple",
        "python_dependencies": "scikit-learn",
        "pkg_pypi_name": "scikit-learn",
        "object_types": ["metric"],
    }

    _obj_dict = {
        "accuracy_score": "sklearn.metrics.accuracy_score",
    }

    _type_of_objs = {
        "accuracy_score": "metric",
    }

    _objs_by_type = {
        "metric": ["accuracy_score"],
    }