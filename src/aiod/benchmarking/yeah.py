from aiod.benchmarking import ClassificationBenchmark

if __name__ == "__main__":
    benchmark = ClassificationBenchmark()

    benchmark.add("RandomForestClassifier(n_estimators=100)")
    benchmark.add("XGBClassifier(n_estimators=100)")
    # benchmark.add("LGBMClassifier(n_estimators=100)")

    benchmark.add("load_iris(return_X_y=True)")
    benchmark.add("KFold(n_splits=2, shuffle=True, random_state=42)")
    benchmark.add("accuracy_score")

    results = benchmark.run()
    print(results.info())