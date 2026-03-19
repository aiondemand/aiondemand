"""Tests for sklearn indexing through the unified updater."""

from pathlib import Path

from aiod.utils._indexing._index_file_utils import _parse_assignment_dict
from aiod.utils._indexing.update_library_indexes import (
	LibraryConfig,
	update_library_index,
)


def _write_model_file(path: Path) -> None:
	path.write_text(
		"""
class AiodPkg__Sklearn:
	_obj_dict = {
		"ExistingEstimator": "sklearn.existing.ExistingEstimator",
		"Pipeline": "sklearn.pipeline.Pipeline",
	}

	_type_of_objs = {
		"ExistingEstimator": "classifier",
		"Pipeline": ["classifier", "transformer"],
	}

	_objs_by_type = {
		"classifier": ["ExistingEstimator", "Pipeline"],
		"transformer": ["Pipeline"],
	}
""".lstrip(),
		encoding="utf-8",
	)


def test_update_library_index_for_sklearn_adds_new_objects(tmp_path):
	model_file = tmp_path / "scikit_learn.py"
	_write_model_file(model_file)

	config = LibraryConfig(
		name="sklearn",
		package_name="sklearn",
		model_file=model_file,
		locdict_fn=lambda package_name: {
			"ExistingEstimator": "sklearn.existing.ExistingEstimator",
			"NewEstimator": "sklearn.new.NewEstimator",
			"Pipeline": "sklearn.pipeline.Pipeline",
		},
		type_fn=lambda package_name: {
			"ExistingEstimator": "classifier",
			"NewEstimator": "regressor",
		},
	)

	result = update_library_index(
		config,
		apply_changes=True,
		skip_missing_files=False,
	)

	assert result.changed is True
	assert result.added_objects == ["NewEstimator"]
	assert result.unknown_types == []

	updated = model_file.read_text(encoding="utf-8")
	obj_dict = _parse_assignment_dict(updated, "_obj_dict")
	type_of_objs = _parse_assignment_dict(updated, "_type_of_objs")
	objs_by_type = _parse_assignment_dict(updated, "_objs_by_type")

	assert obj_dict["NewEstimator"] == "sklearn.new.NewEstimator"
	assert type_of_objs["Pipeline"] == ["classifier", "transformer"]
	assert objs_by_type["regressor"] == ["NewEstimator"]


def test_update_library_index_for_sklearn_reports_unknown_types(tmp_path):
	model_file = tmp_path / "scikit_learn.py"
	_write_model_file(model_file)

	config = LibraryConfig(
		name="sklearn",
		package_name="sklearn",
		model_file=model_file,
		locdict_fn=lambda package_name: {
			"ExistingEstimator": "sklearn.existing.ExistingEstimator",
			"UnknownEstimator": "sklearn.unknown.UnknownEstimator",
		},
		type_fn=lambda package_name: {"ExistingEstimator": "classifier"},
	)

	result = update_library_index(
		config,
		apply_changes=False,
		skip_missing_files=False,
	)

	assert result.changed is True
	assert result.added_objects == ["UnknownEstimator"]
	assert result.unknown_types == ["UnknownEstimator"]


def test_update_library_index_passes_package_to_discovery_functions(tmp_path):
	model_file = tmp_path / "scikit_learn.py"
	_write_model_file(model_file)

	captured = {"locdict_package_name": None, "type_package_name": None}

	def _locdict_fn(package_name: str) -> dict[str, str]:
		captured["locdict_package_name"] = package_name
		return {
			"ExistingEstimator": "custompkg.existing.ExistingEstimator",
			"Pipeline": "custompkg.pipeline.Pipeline",
		}

	def _type_fn(package_name: str) -> dict[str, str | list[str]]:
		captured["type_package_name"] = package_name
		return {
			"ExistingEstimator": "classifier",
			"Pipeline": ["classifier", "transformer"],
		}

	config = LibraryConfig(
		name="custom",
		package_name="custompkg",
		model_file=model_file,
		locdict_fn=_locdict_fn,
		type_fn=_type_fn,
	)

	update_library_index(
		config,
		apply_changes=False,
		skip_missing_files=False,
	)

	assert captured["locdict_package_name"] == "custompkg"
	assert captured["type_package_name"] == "custompkg"