"""Auto-sklearn classifier."""

from aiod.models.apis import _ModelPkgSklearnEstimator


class AiodPkg__AutoSklearnClassifier(_ModelPkgSklearnEstimator):
    _tags = {
        "pkg_id": "AutoSklearnClassifier",
        "python_dependencies": "auto-sklearn",
        "pkg_pypi_name": "auto-sklearn",
    }

    _obj = "autosklearn.classification.AutoSklearnClassifier"
