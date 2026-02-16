"""
"""

import pytest

from aiod.models.classification import AiodPkg__SklearnClassifiers
from aiod.models.cluster import AiodPkg__SklearnClusters
from aiod.models.regression import AiodPkg__SklearnRegressors
from aiod.models.transformation import AiodPkg__SklearnTransformers
from aiod.utils._indexing._preindex_sklearn import _sklearn_estimators_locdict_by_type

@pytest.mark.parametrize(
    "type_filter, pkg_cls",
    [
        ("classifier", AiodPkg__SklearnClassifiers),
        ("regressor", AiodPkg__SklearnRegressors),
        ("cluster", AiodPkg__SklearnClusters),
        ("transformer", AiodPkg__SklearnTransformers),
    ]
)
def test_prebuilt_index_matches_sklearn(type_filter, pkg_cls):
    generated = _sklearn_estimators_locdict_by_type(type_filter)
    prebuilt = pkg_cls.contained_ids()
    assert set(generated.keys()) == set(prebuilt)