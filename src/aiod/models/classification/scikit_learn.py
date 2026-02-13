"""Sklearn classifiers."""

from aiod.models.apis import _ModelPkgClassifier
from aiod.utils._indexing._preindex_sklearn import _sklearn_estimators_locdict_by_type


class AiodPkg__SklearnClassifiers(_ModelPkgClassifier):
    _tags = {
        "pkg_id": "__multiple",
        "python_dependencies": "scikit-learn",
        "pkg_pypi_name": "scikit-learn",
    }

    # obtained via utils._indexing._preindex_sklearn
    # todo: automate generation
    # todo: include version bounds for availability
    # todo: test generated index against actual index
    _obj_dict = _sklearn_estimators_locdict_by_type("classifier")
