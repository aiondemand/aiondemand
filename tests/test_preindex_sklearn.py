"""Test sklearn preindex utilities."""

import pytest
import sys

from aiod.utils._indexing._preindex_sklearn import (
    _all_sklearn_estimators_locdict,
    _generate_sklearn_types_of_obj,
)

#scikit-learn model pkg
from aiod.models.apis import _ModelPkgSklearnEstimator
import aiod.models.sklearn_apis
from skbase.utils.dependencies import _safe_import


def _get_all_sklearn_packages():
    _API_BASE_CLASSES = [_ModelPkgSklearnEstimator]
    _all_subclasses = []
    for base in _API_BASE_CLASSES:
        _all_subclasses.extend(base.__subclasses__())
    pkgs = []
    for cls in _all_subclasses:
        pkg = cls()
        mod = _safe_import(pkg._tags["pkg_pypi_name"])
        if mod is not None:
            pkgs.append(pkg)
        else:
            import warnings
            warnings.warn(
                f"Skipping {pkg.__class__.__name__} because "
                f"{pkg._tags['pkg_pypi_name']} is not installed."
            )
    return pkgs


@pytest.mark.parametrize(
    "package",
    _get_all_sklearn_packages(),
    ids=lambda pkg: pkg.__class__.__name__,
)
def test_sklearn_obj_dict(package):
    """Test that generated sklearn loc dict matches the package _obj_dict."""
    if package._tags["pkg_pypi_name"] == "sklearn" and sys.version_info < (3, 11):
        pytest.skip("ClassicalMDS sklearn estimator not available in Python 3.10")
    loc_dict = _all_sklearn_estimators_locdict(package._tags["pkg_pypi_name"])
    for obj_name, obj_loc in package._obj_dict.items():
        assert obj_name in loc_dict
        assert obj_loc == loc_dict[obj_name]


@pytest.mark.parametrize(
    "package",
    _get_all_sklearn_packages(),
    ids=lambda pkg: pkg.__class__.__name__,
)
def test_sklearn_types_of_obj(package):
    """Test that generated sklearn types dict matches the package _type_of_objs."""
    if package._tags["pkg_pypi_name"] == "sklearn" and sys.version_info < (3, 11):
        pytest.skip("ClassicalMDS sklearn estimator not available in Python 3.10")
    type_dict = _generate_sklearn_types_of_obj(package._tags["pkg_pypi_name"])
    for type_, objs in package._type_of_objs.items():
        assert type_ in type_dict
        assert set(objs) == set(type_dict[type_])
