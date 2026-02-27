"""Tests for ClassificationBenchmark."""

import pytest
from skbase.utils.dependencies import _check_soft_dependencies

sklearn_available = _check_soft_dependencies("scikit-learn", severity="none")

pytestmark = pytest.mark.skipif(
    not sklearn_available,
    reason="run only if scikit-learn is installed",
)


@pytest.fixture
def benchmark():
    """Return a pre-configured ClassificationBenchmark using iris + KFold."""
    from aiod.benchmarking import ClassificationBenchmark

    b = ClassificationBenchmark()
    b.add("RandomForestClassifier(n_estimators=10, random_state=0)")
    b.add("DecisionTreeClassifier(random_state=0)")
    b.add("load_iris(return_X_y=True)")
    b.add("KFold(n_splits=2, shuffle=True, random_state=42)")
    b.add("accuracy_score")
    return b


def test_run_returns_dataframe(benchmark):
    """run() must return a pandas DataFrame."""
    import pandas as pd

    results = benchmark.run()
    assert isinstance(results, pd.DataFrame)


def test_run_column_count_matches_estimators(benchmark):
    """One column per estimator × task combination."""
    results = benchmark.run()
    # 2 estimators × 1 dataset × 1 resampler = 2 columns
    assert results.shape[1] == 2


def test_run_has_required_rows(benchmark):
    """Results index must contain all expected metric/metadata rows."""
    results = benchmark.run()
    required = {
        "task_id",
        "model_id",
        "accuracy_score_mean",
        "accuracy_score_std",
        "fit_time_mean",
        "fit_time_std",
        "pred_time_mean",
        "pred_time_std",
        "runtime_secs",
    }
    assert required.issubset(set(results.index))


def test_run_fold_rows_present(benchmark):
    """Per-fold rows should be present for 2 splits."""
    results = benchmark.run()
    assert "accuracy_score_fold_0_test" in results.index
    assert "accuracy_score_fold_1_test" in results.index
    assert "fit_time_fold_0_test" in results.index
    assert "pred_time_fold_0_test" in results.index


def test_model_id_matches_estimator_name(benchmark):
    """model_id row should contain the estimator class names."""
    results = benchmark.run()
    model_ids = list(results.loc["model_id"])
    assert "RandomForestClassifier" in model_ids
    assert "DecisionTreeClassifier" in model_ids


def test_task_id_format(benchmark):
    """task_id should follow the [dataset=X]_[cv=Y] format."""
    results = benchmark.run()
    for task_id in results.loc["task_id"]:
        assert "[dataset=" in task_id
        assert "[cv=" in task_id


def test_add_dispatch():
    """add() should route specs to the correct internal lists."""
    from aiod.benchmarking import ClassificationBenchmark

    b = ClassificationBenchmark()
    b.add("RandomForestClassifier(n_estimators=100)")
    b.add("load_iris(return_X_y=True)")
    b.add("KFold(n_splits=5)")
    b.add("accuracy_score")

    assert len(b._estimator_specs) == 1
    assert len(b._dataset_specs) == 1
    assert len(b._resampler_specs) == 1
    assert len(b._metric_specs) == 1


def test_add_raises_with_invalid_component():
    """add() must raise ValueError immediately if component is not in registry."""
    from aiod.benchmarking import ClassificationBenchmark

    b = ClassificationBenchmark()
    with pytest.raises(ValueError, match="not found in aiod registry"):
        b.add("NonExistentClassifier()")


def test_run_raises_with_missing_components():
    """run() must raise ValueError if any component list is empty."""
    from aiod.benchmarking import ClassificationBenchmark

    b = ClassificationBenchmark()
    # add only estimator, but use a valid one to avoid add() failing
    b.add("RandomForestClassifier(n_estimators=10)")
    # no dataset, resampler, or metric added
    with pytest.raises(ValueError, match="no"):
        b.run()
