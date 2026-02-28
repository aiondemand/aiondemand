"""Tests for preindex generation utilities."""

import pytest

from aiod.utils._indexing import generate_sklearn_index_source
from aiod.utils._indexing._preindex_sklearn import (
	_all_sklearn_estimators_locdict,
	_generate_sklearn_objs_by_type,
	_generate_sklearn_types_of_obj,
)


pytest.importorskip("sklearn")


def test_generate_sklearn_index_source_multiple_contains_core_fragments():
	source = generate_sklearn_index_source()

	assert "class AiodPkg__Sklearn(_ModelPkgSklearnEstimator):" in source
	assert '"pkg_id": "__multiple"' in source
	assert '"python_dependencies": "scikit-learn"' in source
	assert "_obj_dict" in source
	assert "_type_of_objs" in source
	assert "_objs_by_type" in source


def test_generate_sklearn_index_source_multiple_exec_matches_utils():
	source = generate_sklearn_index_source()
	namespace = {}

	exec(source, namespace)

	generated_cls = namespace["AiodPkg__Sklearn"]

	expected_obj_dict = _all_sklearn_estimators_locdict(package_name="sklearn")
	expected_type_of_objs = _generate_sklearn_types_of_obj()
	expected_objs_by_type = _generate_sklearn_objs_by_type(expected_type_of_objs)

	assert generated_cls._obj_dict == expected_obj_dict
	assert generated_cls._type_of_objs == expected_type_of_objs
	assert generated_cls._objs_by_type == expected_objs_by_type


def test_generate_sklearn_index_source_single_mode_contains_single_class_entries():
	source = generate_sklearn_index_source(mode="single")

	assert "class AiodPkg__RandomForestClassifier(_ModelPkgSklearnEstimator):" in source
	assert '"pkg_id": "RandomForestClassifier"' in source
	assert '"pkg_pypi_name": "scikit-learn"' in source
	assert '_obj = "sklearn.ensemble.RandomForestClassifier"' in source