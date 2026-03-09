"""Test script for benchmarking add() and run()."""

from aiod.benchmarking.classification import ClassificationBenchmark
from pathlib import Path

def test_full_benchmark_run(tmp_path="./src/aiod/benchmarking/tests/"):
    print("Beginning benchmark run...")
    
    benchmark = ClassificationBenchmark()

    benchmark.add("DecisionTreeClassifier(random_state=42)")
    benchmark.add("RandomForestClassifier(n_estimators=10, random_state=42)")
    
    benchmark.add("accuracy_score")
    benchmark.add("load_iris")
    benchmark.add("KFold(n_splits=2)")

    print("Components added successfully. Running benchmark...")
    results_df = benchmark.run()
    
    print("\nBenchmark completed successfully!\n")
    print("Results DataFrame:")
    print(results_df)

    results_file = Path(tmp_path) / "results.csv"
    results_df.to_csv(results_file)
    assert results_file.exists()