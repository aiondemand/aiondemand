"""Auto-sklearn classifier."""

from aiod.models.apis import _ModelPkgClassifier


class AiodPkg__AutoSklearnClassifier(_ModelPkgClassifier):
    _tags = {
        "pkg_id": "AutoSklearnClassifier",
        "python_dependencies": "auto-sklearn",
        "pkg_pypi_name": "auto-sklearn",
    }

    _obj = "autosklearn.classification.AutoSklearnClassifier"
