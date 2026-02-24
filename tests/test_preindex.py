"""Test preindex utilities and model package indices."""

import pytest
import importlib

from aiod.utils._indexing._preindex_sklearn import (
    _all_sklearn_estimators,
    _all_sklearn_estimators_locdict,
    _generate_sklearn_types_of_obj,
)
from aiod.utils._indexing._preindex import _generate_objs_by_type
from aiod.models.sklearn_apis.scikit_learn import AiodPkg__Sklearn


class TestCommonIndexing:
    """Test the common preindex utility."""

    @pytest.mark.parametrize("package", [
        AiodPkg__Sklearn(),
    ])
    def test_generation_object_by_types(self, package):
        """Test generation of object by types."""
        assert hasattr(package, '_type_of_objs')
        result = _generate_objs_by_type(package._type_of_objs)
        assert result.keys() == package._objs_by_type.keys()

        for obj_type in package._objs_by_type:
            expected_set = set(package._objs_by_type[obj_type])
            actual_set = set(result[obj_type])

            assert expected_set == actual_set


class TestSklearnPreIndex:
    """Test sklearn indexing utilities."""

    def test_sklearn_obj_dict(self):
        """Test generation of sklearn object dict."""
        loc_dict = _all_sklearn_estimators_locdict()
        assert AiodPkg__Sklearn()._obj_dict == loc_dict

    def test_sklearn_types_of_obj(self):
        """Test generation of sklearn types of object."""
        type_dict = _generate_sklearn_types_of_obj()
        assert AiodPkg__Sklearn()._type_of_objs == type_dict
    
    def test_all_estimators_are_indexed(self):
        """Test that all sklearn estimators are indexed in the object dict."""
        all_est= _all_sklearn_estimators()
        obj_dict = AiodPkg__Sklearn()._obj_dict
        for est in all_est:
            est_name = est[0]
            assert est_name in obj_dict, f"{est_name} not indexed"
            est_path = obj_dict[est_name]
            module_name, class_name = est_path.rsplit('.', 1)
            module = importlib.import_module(module_name)
            assert hasattr(module, class_name), f"{class_name} not found in {module_name}"
