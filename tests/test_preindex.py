"""Tests for sklearn preindex updater utilities."""

from pathlib import Path

from aiod.utils._indexing import update_sklearn_index as updater


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


def test_update_sklearn_index_file_adds_new_objects(monkeypatch, tmp_path):
	model_file = tmp_path / "scikit_learn.py"
	_write_model_file(model_file)

	monkeypatch.setattr(
		updater,
		"_all_sklearn_estimators_locdict",
		lambda package_name="sklearn": {
			"ExistingEstimator": "sklearn.existing.ExistingEstimator",
			"NewEstimator": "sklearn.new.NewEstimator",
			"Pipeline": "sklearn.pipeline.Pipeline",
		},
	)
	monkeypatch.setattr(
		updater,
		"_generate_sklearn_types_of_obj",
		lambda package_name="sklearn": {
			"ExistingEstimator": "classifier",
			"NewEstimator": "regressor",
		},
	)

	result = updater.update_sklearn_index_file(
		model_file=model_file, apply_changes=True
	)

	assert result.changed is True
	assert result.added_objects == ["NewEstimator"]
	assert result.unknown_types == []

	updated = model_file.read_text(encoding="utf-8")
	obj_dict = updater._parse_assignment_dict(updated, "_obj_dict")
	type_of_objs = updater._parse_assignment_dict(updated, "_type_of_objs")
	objs_by_type = updater._parse_assignment_dict(updated, "_objs_by_type")

	assert obj_dict["NewEstimator"] == "sklearn.new.NewEstimator"
	assert type_of_objs["Pipeline"] == ["classifier", "transformer"]
	assert objs_by_type["regressor"] == ["NewEstimator"]


def test_update_sklearn_index_file_reports_unknown_types(monkeypatch, tmp_path):
	model_file = tmp_path / "scikit_learn.py"
	_write_model_file(model_file)

	monkeypatch.setattr(
		updater,
		"_all_sklearn_estimators_locdict",
		lambda package_name="sklearn": {
			"ExistingEstimator": "sklearn.existing.ExistingEstimator",
			"UnknownEstimator": "sklearn.unknown.UnknownEstimator",
		},
	)
	monkeypatch.setattr(
		updater,
		"_generate_sklearn_types_of_obj",
		lambda package_name="sklearn": {"ExistingEstimator": "classifier"},
	)

	result = updater.update_sklearn_index_file(
		model_file=model_file, apply_changes=False
	)

	assert result.changed is True
	assert result.added_objects == ["UnknownEstimator"]
	assert result.unknown_types == ["UnknownEstimator"]


def test_update_sklearn_index_file_passes_package_to_type_discovery(
	monkeypatch, tmp_path
):
	model_file = tmp_path / "scikit_learn.py"
	_write_model_file(model_file)

	captured = {"package_name": None}

	monkeypatch.setattr(
		updater,
		"_all_sklearn_estimators_locdict",
		lambda package_name="sklearn": {
			"ExistingEstimator": "custompkg.existing.ExistingEstimator",
			"Pipeline": "custompkg.pipeline.Pipeline",
		},
	)

	def _fake_generate_types(package_name="sklearn"):
		captured["package_name"] = package_name
		return {
			"ExistingEstimator": "classifier",
			"Pipeline": ["classifier", "transformer"],
		}

	monkeypatch.setattr(updater, "_generate_sklearn_types_of_obj", _fake_generate_types)

	updater.update_sklearn_index_file(
		model_file=model_file,
		package_name="custompkg",
		apply_changes=False,
	)

	assert captured["package_name"] == "custompkg"