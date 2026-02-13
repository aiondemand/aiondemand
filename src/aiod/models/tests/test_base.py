"""Test base package class."""

import pytest
from aiod.models.base._base import _AiodModelPkg


class MockSinglePkg(_AiodModelPkg):
    _tags = {"pkg_id": "SingleIDModel"}
    _obj = "some.path"


class MockMultiPkg(_AiodModelPkg):
    _tags = {"pkg_id": "__multiple"}
    _obj_dict = {"ModelA": "path.a", "ModelB": "path.b"}


class TestBasePackage:
    def test_contained_ids_single(self):
        """Test logic when pkg_id is a single string."""
        pkg = MockSinglePkg()
        ids = pkg.contained_ids()
        assert ids == ["SingleIDModel"]

    def test_contained_ids_multiple(self):
        """Test logic when pkg_id is '__multiple'."""
        pkg = MockMultiPkg()
        ids = pkg.contained_ids()
        assert "ModelA" in ids
        assert "ModelB" in ids
        assert len(ids) == 2

    def test_materialize_error(self):
        """
        Test that materialize raises ValueError if _obj is None
        and logic isn't implemented.
        """
        pkg = MockSinglePkg()
        pkg._obj = None  # Simulate missing object

        with pytest.raises(ValueError, match="Error in materialize"):
            pkg._materialize()
