"""Imbalanced-Learn Estimators."""

from aiod.models.apis import _ModelPkgSklearnEstimator


class AiodPkg__ImbalancedLearn(_ModelPkgSklearnEstimator):
    _CLASSES_TO_IGNORE = ["ValueDifferenceMetric"]  # The only metric class

    _tags = {
        "pkg_id": "__multiple",
        "python_dependencies": "imbalanced-learn",
        "pkg_pypi_name": "imblearn",
        "object_types": [],  # needs update
    }
