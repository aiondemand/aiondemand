"""Sklearn clusters."""

from aiod.models.apis import _ModelPkgCluster
from aiod.utils._indexing._preindex_sklearn import _sklearn_estimators_locdict_by_type


class AiodPkg__SklearnClusters(_ModelPkgCluster):
    _tags = {
        "pkg_id": "__multiple",
        "python_dependencies": "scikit-learn",
        "pkg_pypi_name": "scikit-learn",
    }

    _obj_dict = _sklearn_estimators_locdict_by_type("cluster")