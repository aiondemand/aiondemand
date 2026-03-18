"""Tests for multi-library index updater."""

from pathlib import Path

from aiod.utils._indexing.update_library_indexes import (
    LibraryConfig,
    update_library_index,
)
from aiod.utils._indexing.update_sklearn_index import _parse_assignment_dict


def _write_model_file(path: Path) -> None:
    path.write_text(
        """
class AiodPkg__Any:
    _obj_dict = {
        "ExistingEstimator": "pkg.existing.ExistingEstimator",
    }

    _type_of_objs = {
        "ExistingEstimator": "classifier",
    }

    _objs_by_type = {
        "classifier": ["ExistingEstimator"],
    }
""".lstrip(),
        encoding="utf-8",
    )


def test_update_library_index_skips_missing_file(tmp_path):
    config = LibraryConfig(
        name="dummy",
        package_name="dummy",
        model_file=tmp_path / "missing.py",
        locdict_fn=lambda package_name: {},
        type_fn=lambda package_name: {},
    )

    result = update_library_index(
        config,
        apply_changes=False,
        skip_missing_files=True,
    )

    assert result.skipped is True
    assert result.changed is False
    assert "model file not found" in (result.reason or "")


def test_update_library_index_applies_updates(tmp_path):
    model_file = tmp_path / "model.py"
    _write_model_file(model_file)

    config = LibraryConfig(
        name="dummy",
        package_name="dummy",
        model_file=model_file,
        locdict_fn=lambda package_name: {
            "ExistingEstimator": "pkg.existing.ExistingEstimator",
            "NewEstimator": "pkg.new.NewEstimator",
        },
        type_fn=lambda package_name: {
            "ExistingEstimator": "classifier",
            "NewEstimator": ["classifier", "regressor"],
        },
    )

    result = update_library_index(
        config,
        apply_changes=True,
        skip_missing_files=False,
    )

    assert result.skipped is False
    assert result.changed is True
    assert result.added_objects == ["NewEstimator"]
    assert result.unknown_types == []

    text = model_file.read_text(encoding="utf-8")
    assert "NewEstimator" in text
    assert "regressor" in text


def _write_pr_style_model_file(path: Path) -> None:
    path.write_text(
        """
class AiodPkg__Any:
    _obj_dict = {
        "ExistingEstimator": "pkg.existing.ExistingEstimator",
    }

    _type_of_objs = {
        "ExistingEstimator": "classifier",
    }

    _objs_by_type = {
        "classifier": ["ExistingEstimator"],
    }
""".lstrip(),
        encoding="utf-8",
    )


def test_update_library_index_sktime_pr_shape(tmp_path):
    model_file = tmp_path / "sktime.py"
    _write_pr_style_model_file(model_file)

    config = LibraryConfig(
        name="sktime",
        package_name="sktime",
        model_file=model_file,
        locdict_fn=lambda package_name: {
            "ARIMA": "sktime.forecasting.arima._pmdarima.ARIMA",
            "CutoffSplitter": "sktime.split.cutoff.CutoffSplitter",
            "WindowedF1Score": (
                "sktime.performance_metrics.detection._f1score.WindowedF1Score"
            ),
            "ForecastingGridSearchCV": (
                "sktime.forecasting.model_selection._gridsearch."
                "ForecastingGridSearchCV"
            ),
        },
        type_fn=lambda package_name: {
            "ARIMA": "forecaster",
            "CutoffSplitter": "splitter",
            "WindowedF1Score": "metric_detection",
            "ForecastingGridSearchCV": "forecaster",
        },
    )

    result = update_library_index(
        config,
        apply_changes=True,
        skip_missing_files=False,
    )

    assert result.changed is True
    assert sorted(result.added_objects) == [
        "ARIMA",
        "CutoffSplitter",
        "ForecastingGridSearchCV",
        "WindowedF1Score",
    ]
    assert result.unknown_types == []

    updated = model_file.read_text(encoding="utf-8")
    obj_dict = _parse_assignment_dict(updated, "_obj_dict")
    type_of_objs = _parse_assignment_dict(updated, "_type_of_objs")
    objs_by_type = _parse_assignment_dict(updated, "_objs_by_type")

    assert obj_dict["ARIMA"] == "sktime.forecasting.arima._pmdarima.ARIMA"
    assert type_of_objs["CutoffSplitter"] == "splitter"
    assert objs_by_type["forecaster"] == ["ARIMA", "ForecastingGridSearchCV"]
    assert objs_by_type["metric_detection"] == ["WindowedF1Score"]
    assert objs_by_type["splitter"] == ["CutoffSplitter"]


def test_update_library_index_skpro_pr_shape(tmp_path):
    model_file = tmp_path / "skpro.py"
    _write_pr_style_model_file(model_file)

    config = LibraryConfig(
        name="skpro",
        package_name="skpro",
        model_file=model_file,
        locdict_fn=lambda package_name: {
            "Pipeline": "skpro.compose._pipeline.Pipeline",
            "CRPS": "skpro.metrics._classes.CRPS",
            "MAPIERegressor": "skpro.regression.mapie.MAPIERegressor",
        },
        type_fn=lambda package_name: {
            "Pipeline": ["regressor_proba", "transformer"],
            "CRPS": "metric_proba",
            "MAPIERegressor": "regressor_proba",
        },
    )

    result = update_library_index(
        config,
        apply_changes=True,
        skip_missing_files=False,
    )

    assert result.changed is True
    assert sorted(result.added_objects) == ["CRPS", "MAPIERegressor", "Pipeline"]
    assert result.unknown_types == []

    updated = model_file.read_text(encoding="utf-8")
    type_of_objs = _parse_assignment_dict(updated, "_type_of_objs")
    objs_by_type = _parse_assignment_dict(updated, "_objs_by_type")

    assert type_of_objs["Pipeline"] == ["regressor_proba", "transformer"]
    assert objs_by_type["metric_proba"] == ["CRPS"]
    assert objs_by_type["regressor_proba"] == ["MAPIERegressor", "Pipeline"]
    assert objs_by_type["transformer"] == ["Pipeline"]


def test_update_library_index_hyperactive_pr_shape(tmp_path):
    model_file = tmp_path / "hyperactive.py"
    _write_pr_style_model_file(model_file)

    config = LibraryConfig(
        name="hyperactive",
        package_name="hyperactive",
        model_file=model_file,
        locdict_fn=lambda package_name: {
            "BayesianOptimizer": (
                "hyperactive.opt.gfo.bayesian_optimizer.BayesianOptimizer"
            ),
            "RandomSearch": "hyperactive.opt.gfo.random_search.RandomSearch",
            "SimulatedAnnealing": (
                "hyperactive.opt.gfo.simulated_annealing.SimulatedAnnealing"
            ),
        },
        type_fn=lambda package_name: {
            "BayesianOptimizer": "optimizer",
            "RandomSearch": "optimizer",
            "SimulatedAnnealing": "optimizer",
        },
    )

    result = update_library_index(
        config,
        apply_changes=True,
        skip_missing_files=False,
    )

    assert result.changed is True
    assert sorted(result.added_objects) == [
        "BayesianOptimizer",
        "RandomSearch",
        "SimulatedAnnealing",
    ]
    assert result.unknown_types == []

    updated = model_file.read_text(encoding="utf-8")
    type_of_objs = _parse_assignment_dict(updated, "_type_of_objs")
    objs_by_type = _parse_assignment_dict(updated, "_objs_by_type")

    assert type_of_objs["BayesianOptimizer"] == "optimizer"
    assert objs_by_type["optimizer"] == [
        "BayesianOptimizer",
        "RandomSearch",
        "SimulatedAnnealing",
    ]
