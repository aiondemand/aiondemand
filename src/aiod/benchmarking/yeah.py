from aiod.benchmarking import ClassificationBenchmark

if __name__ == "__main__":
    benchmark = ClassificationBenchmark()

    # Estimators from AiodPkg__Sklearn and AiodPkg__XGBClassifier
    benchmark.add("RandomForestClassifier(n_estimators=100)")
    benchmark.add("XGBClassifier(n_estimators=100)")

    # Dataset from AiodPkg__SklearnDatasets
    benchmark.add("load_iris(return_X_y=True)")

    # Resamplers from AiodPkg__SklearnResamplers
    benchmark.add("KFold(n_splits=2, shuffle=True, random_state=42)")

    # Metrics from AiodPkg__SklearnMetrics
    benchmark.add("accuracy_score")

    results = benchmark.run()
    print(results.to_string())
