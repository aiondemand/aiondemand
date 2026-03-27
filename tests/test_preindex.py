"""Test common preindex utilities."""

import pytest

from aiod.utils._indexing._preindex import _generate_objs_by_type
from skbase.lookup import all_objects

#part 1
from aiod.models.apis import _ModelPkgSklearnEstimator
import aiod.models.sklearn_apis


_API_BASE_CLASSES = [_ModelPkgSklearnEstimator,]

_all_subclasses = []
for base in _API_BASE_CLASSES:
    _all_subclasses.extend(base.__subclasses__())

_all_packages = [cls() for cls in _all_subclasses]


@pytest.mark.parametrize(
    "package",
    _all_packages,
    ids=[pkg.__class__.__name__ for pkg in _all_packages],
)
def test_generated_objs_by_type(package):
    """Test that generated sklearn objs by type matches the package _objs_by_type."""
    objs_by_type = _generate_objs_by_type(package._type_of_objs)
    for type_, objs in package._objs_by_type.items():
        assert type_ in objs_by_type
        assert set(objs) == set(objs_by_type[type_])
