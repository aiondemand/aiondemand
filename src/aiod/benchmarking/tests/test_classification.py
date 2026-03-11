"""Test script for benchmarking add() and run()."""

from pathlib import Path

from aiod.benchmarking.classification import ClassificationBenchmark


def test_full_benchmark_run(tmp_path="./src/aiod/benchmarking/tests/"):
    benchmark = ClassificationBenchmark()

    benchmark.add("DecisionTreeClassifier(random_state=42)")
    benchmark.add("RandomForestClassifier(n_estimators=10, random_state=42)")
    
    benchmark.add("accuracy_score")
    benchmark.add("load_iris")
    benchmark.add("KFold(n_splits=2)")
    results_df = benchmark.run()

    results_file = Path(tmp_path) / "results.csv"
    results_df.to_csv(results_file)
    assert results_file.exists()