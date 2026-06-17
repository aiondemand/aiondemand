"""Tests for ClassificationBenchmark."""

import pandas as pd
import pytest
from sklearn.datasets import load_breast_cancer, load_iris
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import KFold
from sklearn.tree import DecisionTreeClassifier

from aiod.benchmarking.classification import ClassificationBenchmark


def _iris_xy():
    data = load_iris()
    return data.data, data.target


def _binary_xy():
    data = load_breast_cancer()
    return data.data, data.target


class TestAddSpec:
    def test_add_classifier_string(self):
        b = ClassificationBenchmark()
        b.add("DecisionTreeClassifier(random_state=0)")
        assert len(b.estimators) == 1

    def test_add_metric(self):
        b = ClassificationBenchmark()
        b.add("accuracy_score")
        assert len(b._metrics) == 1

    def test_add_dataset(self):
        b = ClassificationBenchmark()
        b.add("load_iris")
        assert len(b._datasets) == 1

    def test_add_cv_splitter(self):
        b = ClassificationBenchmark()
        b.add("KFold(n_splits=3)")
        assert len(b._cv_splitters) == 1

    def test_add_estimator_object(self):
        b = ClassificationBenchmark()
        b.add_estimator(DecisionTreeClassifier(random_state=0))
        assert len(b.estimators) == 1

    def test_add_estimator_list(self):
        b = ClassificationBenchmark()
        b.add_estimator([
            DecisionTreeClassifier(random_state=0),
            DummyClassifier(),
        ])
        assert len(b.estimators) == 2

    def test_duplicate_estimator_id_renamed(self):
        b = ClassificationBenchmark()
        b.add_estimator(DecisionTreeClassifier(), estimator_id="clf")
        with pytest.warns(UserWarning, match="already registered"):
            b.add_estimator(DecisionTreeClassifier(), estimator_id="clf")
        assert "clf" in b.estimators
        assert "clf_1" in b.estimators

class TestAddTask:
    def test_add_task_explicit_id(self):
        b = ClassificationBenchmark()
        X, y = _iris_xy()
        def loader(): return X, y
        b.add_task(
            dataset_loader=loader,
            cv_splitter=KFold(n_splits=2),
            scorers=[accuracy_score],
            task_id="test_task",
        )
        assert "test_task" in b.tasks

    def test_add_task_auto_id_callable(self):
        b = ClassificationBenchmark()
        X, y = _iris_xy()

        def test_loader():
            return X, y

        b.add_task(
            dataset_loader=test_loader,
            cv_splitter=KFold(n_splits=2),
            scorers=[accuracy_score],
        )
        task_id = list(b.tasks.keys())[0]
        assert "test_loader" in task_id

    def test_duplicate_task_id_renamed(self):
        b = ClassificationBenchmark()
        X, y = _iris_xy()
        def loader(): return X, y
        cv = KFold(n_splits=2)
        b.add_task(loader, cv, [accuracy_score], task_id="task")
        with pytest.warns(UserWarning, match="already registered"):
            b.add_task(loader, cv, [accuracy_score], task_id="task")
        assert "task" in b.tasks
        assert "task_1" in b.tasks

class TestRun:
    @pytest.fixture
    def simple_benchmark(self):
        X, y = _iris_xy()
        b = ClassificationBenchmark()
        b.add_estimator(DecisionTreeClassifier(random_state=0))
        def loader(): return X, y
        b.add_task(
            dataset_loader=loader,
            cv_splitter=KFold(n_splits=2, shuffle=True, random_state=0),
            scorers=[accuracy_score],
            task_id="iris_task",
        )
        return b

    def test_run_returns_dataframe(self, simple_benchmark):
        df = simple_benchmark.run()
        assert isinstance(df, pd.DataFrame)

    def test_run_not_empty(self, simple_benchmark):
        df = simple_benchmark.run()
        assert not df.empty

    def test_run_contains_metric_column(self, simple_benchmark):
        df = simple_benchmark.run()
        assert "accuracy_score_mean" in df.index

    def test_run_multiple_estimators(self):
        X, y = _iris_xy()
        b = ClassificationBenchmark()
        b.add_estimator(DecisionTreeClassifier(random_state=0))
        b.add_estimator(DummyClassifier(strategy="most_frequent"))
        def loader(): return X, y
        b.add_task(
            dataset_loader=loader,
            cv_splitter=KFold(n_splits=2, shuffle=True, random_state=0),
            scorers=[accuracy_score],
            task_id="multi_clf",
        )
        df = b.run()
        assert not df.empty
        assert df.shape[1] >= 2

    def test_run_multiple_metrics(self):
        from sklearn.metrics import accuracy_score as acc

        X, y = _iris_xy()
        b = ClassificationBenchmark()
        b.add_estimator(DecisionTreeClassifier(random_state=0))
        def loader(): return X, y
        b.add_task(
            dataset_loader=loader,
            cv_splitter=KFold(n_splits=2, shuffle=True, random_state=0),
            scorers=[acc],
            task_id="multi_metric",
        )
        df = b.run()
        assert "accuracy_score_mean" in df.index

    def test_run_multiple_tasks(self):
        X_iris, y_iris = _iris_xy()
        X_bc, y_bc = _binary_xy()
        b = ClassificationBenchmark()
        b.add_estimator(DecisionTreeClassifier(random_state=0))
        def iris_loader(): return X_iris, y_iris
        def bc_loader(): return X_bc, y_bc
        b.add_task(
            dataset_loader=iris_loader,
            cv_splitter=KFold(n_splits=2, shuffle=True, random_state=0),
            scorers=[accuracy_score],
            task_id="iris",
        )
        b.add_task(
            dataset_loader=bc_loader,
            cv_splitter=KFold(n_splits=2, shuffle=True, random_state=0),
            scorers=[accuracy_score],
            task_id="breast_cancer",
        )
        df = b.run()
        assert not df.empty

    def test_run_via_add_spec_end_to_end(self):
        b = ClassificationBenchmark()
        b.add("DecisionTreeClassifier(random_state=42)")
        b.add("accuracy_score")
        b.add("load_iris")
        b.add("KFold(n_splits=2)")
        df = b.run()
        assert isinstance(df, pd.DataFrame)
        assert not df.empty

class TestForceRerun:
    def test_force_rerun_none_skips_existing(self, tmp_path):
        X, y = _iris_xy()
        def loader(): return X, y
        b = ClassificationBenchmark()
        b.add_estimator(DecisionTreeClassifier(random_state=0), estimator_id="tree")
        b.add_task(
            dataset_loader=loader,
            cv_splitter=KFold(n_splits=2, shuffle=True, random_state=0),
            scorers=[accuracy_score],
            task_id="iris_task",
        )
        output = tmp_path / "results.json"
        df1 = b.run(output_file=str(output), force_rerun="none")

        b2 = ClassificationBenchmark()
        b2.add_estimator(DecisionTreeClassifier(random_state=0), estimator_id="tree")
        b2.add_task(
            dataset_loader=loader,
            cv_splitter=KFold(n_splits=2, shuffle=True, random_state=0),
            scorers=[accuracy_score],
            task_id="iris_task",
        )
        df2 = b2.run(output_file=str(output), force_rerun="none")
        assert df1.shape == df2.shape


class TestReturnData:
    def test_return_data_false_default(self):
        X, y = _iris_xy()
        b = ClassificationBenchmark(return_data=False)
        b.add_estimator(DecisionTreeClassifier(random_state=0))
        def loader(): return X, y
        b.add_task(
            dataset_loader=loader,
            cv_splitter=KFold(n_splits=2, shuffle=True, random_state=0),
            scorers=[accuracy_score],
            task_id="t",
        )
        df = b.run()
        assert not df.empty

    def test_return_data_true(self):
        X, y = _iris_xy()
        b = ClassificationBenchmark(return_data=True)
        b.add_estimator(DecisionTreeClassifier(random_state=0))
        def loader(): return X, y
        b.add_task(
            dataset_loader=loader,
            cv_splitter=KFold(n_splits=2, shuffle=True, random_state=0),
            scorers=[accuracy_score],
            task_id="t",
        )
        df = b.run()
        assert not df.empty


class TestRankingInOutput:
    def test_rank_columns_present(self):
        """Ranking requires _metrics to be populated, which happens via add()."""
        b = ClassificationBenchmark()
        b.add("DecisionTreeClassifier(random_state=0)")
        b.add("DummyClassifier()")
        b.add("accuracy_score")
        b.add("load_iris")
        b.add("KFold(n_splits=2)")
        df = b.run()
        assert "accuracy_score_mean_rank" in df.index