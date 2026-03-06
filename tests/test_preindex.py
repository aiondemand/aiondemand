"""Test preindex utilities and model package indices."""

import pytest
import importlib
import sys

from aiod.utils._indexing._preindex_sklearn import (
    _all_sklearn_estimators,
    _all_sklearn_estimators_locdict,
    _generate_sklearn_types_of_obj,
)
from aiod.utils._indexing._preindex import _generate_objs_by_type

#part 1
from aiod.models.apis import _ModelPkgSklearnEstimator
import aiod.models.sklearn_apis

@pytest.mark.skipif(
    sys.version_info < (3, 11),
    reason="ClassicalMDS sklearn estimator not available in Python 3.10",
)
class TestPreindex:
    # new apis added here
    _API_BASE_CLASSES = [_ModelPkgSklearnEstimator]

    _all_subclasses = []
    for base in _API_BASE_CLASSES:
        _all_subclasses.extend(base.__subclasses__())

    _all_packages = [cls() for cls in _all_subclasses]

    """Test sklearn-specific preindex generation utilities."""

    @pytest.mark.parametrize(
        "package",
        _all_packages,
        ids=[pkg.__class__.__name__ for pkg in _all_packages],

    )
    def test_generated_objs_by_type(self, package):
        """Test that generated sklearn objs by type matches the package _objs_by_type."""
        objs_by_type = _generate_objs_by_type(package._type_of_objs)
        assert package._objs_by_type == objs_by_type

    @pytest.mark.parametrize(
        "package",
        _all_packages,
        ids=[pkg.__class__.__name__ for pkg in _all_packages],

    )
    def test_sklearn_obj_dict(self, package):
        """Test that generated sklearn loc dict matches the package _obj_dict."""
        loc_dict = _all_sklearn_estimators_locdict(package._tags['pkg_pypi_name'])
        assert package._obj_dict.keys() == loc_dict.keys()

    @pytest.mark.parametrize(
        "package",
        _all_packages,
        ids=[pkg.__class__.__name__ for pkg in _all_packages],
    )
    def test_sklearn_types_of_obj(self, package):
        """Test that generated sklearn types dict matches the package _type_of_objs."""
        type_dict = _generate_sklearn_types_of_obj(package._tags['pkg_pypi_name'])
        assert package._type_of_objs.keys() == type_dict.keys()
