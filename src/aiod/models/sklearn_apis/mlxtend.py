# ruff: noqa: E501
"""mlxtend model package."""

from aiod.models.apis import _ModelPkgSklearnEstimator


class AiodPkg__Mlxtend(_ModelPkgSklearnEstimator):
    _tags = {
        "pkg_id": "__multiple",
        "python_dependencies": "mlxtend",
        "pkg_pypi_name": "mlxtend",
        "object_types": ["classifier", "regressor"],
    }

    _obj_dict = {
        "Adaline": "mlxtend.classifier.adaline.Adaline",
        "EnsembleVoteClassifier": "mlxtend.classifier.ensemble_vote.EnsembleVoteClassifier",
        "LogisticRegression": "mlxtend.classifier.logistic_regression.LogisticRegression",
        "MultiLayerPerceptron": "mlxtend.classifier.multilayerperceptron.MultiLayerPerceptron",
        "OneRClassifier": "mlxtend.classifier.oner.OneRClassifier",
        "Perceptron": "mlxtend.classifier.perceptron.Perceptron",
        "SoftmaxRegression": "mlxtend.classifier.softmax_regression.SoftmaxRegression",
        "StackingCVClassifier": "mlxtend.classifier.stacking_cv_classification.StackingCVClassifier",
        "StackingClassifier": "mlxtend.classifier.stacking_classification.StackingClassifier",
        "ColumnSelector": "mlxtend.feature_selection.column_selector.ColumnSelector",
        "ExhaustiveFeatureSelector": "mlxtend.feature_selection.exhaustive_feature_selector.ExhaustiveFeatureSelector",
        "SequentialFeatureSelector": "mlxtend.feature_selection.sequential_feature_selector.SequentialFeatureSelector",
        "CopyTransformer": "mlxtend.preprocessing.copy_transformer.CopyTransformer",
        "DenseTransformer": "mlxtend.preprocessing.dense_transformer.DenseTransformer",
        "TransactionEncoder": "mlxtend.preprocessing.transactionencoder.TransactionEncoder",
        "StackingCVRegressor": "mlxtend.regressor.stacking_cv_regression.StackingCVRegressor",
        "StackingRegressor": "mlxtend.regressor.stacking_regression.StackingRegressor",
    }

    _type_of_objs = {
        "Adaline": "classifier",
        "EnsembleVoteClassifier": ["transformer", "classifier"],
        "LogisticRegression": "classifier",
        "MultiLayerPerceptron": "classifier",
        "OneRClassifier": "classifier",
        "Perceptron": "classifier",
        "SoftmaxRegression": "classifier",
        "StackingCVClassifier": "classifier",
        "StackingClassifier": "classifier",
        "ColumnSelector": "transformer",
        "ExhaustiveFeatureSelector": "transformer",
        "SequentialFeatureSelector": "transformer",
        "CopyTransformer": "transformer",
        "DenseTransformer": "transformer",
        "TransactionEncoder": "transformer",
        "StackingCVRegressor": ["transformer", "regressor"],
        "StackingRegressor": ["transformer", "regressor"],
    }

    _objs_by_type = {
        "classifier": [
            "Adaline",
            "EnsembleVoteClassifier",
            "LogisticRegression",
            "MultiLayerPerceptron",
            "OneRClassifier",
            "Perceptron",
            "SoftmaxRegression",
            "StackingCVClassifier",
            "StackingClassifier",
        ],
        "transformer": [
            "EnsembleVoteClassifier",
            "ColumnSelector",
            "ExhaustiveFeatureSelector",
            "SequentialFeatureSelector",
            "CopyTransformer",
            "DenseTransformer",
            "TransactionEncoder",
            "StackingCVRegressor",
            "StackingRegressor",
        ],
        "regressor": ["StackingCVRegressor", "StackingRegressor"],
    }
