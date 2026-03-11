"""Feature-Engine Estimators."""

from aiod.models.apis import _ModelPkgSklearnEstimator


class AiodPkg__FeatureEngine(_ModelPkgSklearnEstimator):
    _tags = {
        "pkg_id": "__multiple",
        "python_dependencies": "feature-engine",
        "pkg_pypi_name": "feature_engine",
        "object_types": [],  # needs update
    }
