# ruff: noqa: E501
"""mlxtend model package."""

from aiod.models.apis import _ModelPkgSklearnEstimator


class AiodPkg__mlxtend(_ModelPkgSklearnEstimator):
    _tags = {
        "pkg_id": "__multiple",
        "python_dependencies": "mlxtend",
        "pkg_pypi_name": "mlxtend",
        "object_types": ["classifier", "regressor"],
    }

    _obj_dict = {
        "ColumnSelector": "mlxtend.feature_selection.column_selector.ColumnSelector",
        "CopyTransformer": "mlxtend.preprocessing.copy_transformer.CopyTransformer",
        "DenseTransformer": "mlxtend.preprocessing.dense_transformer.DenseTransformer",
        "EnsembleVoteClassifier": "mlxtend.classifier.ensemble_vote.EnsembleVoteClassifier",
        "ExhaustiveFeatureSelector": "mlxtend.feature_selection.exhaustive_feature_selector.ExhaustiveFeatureSelector",
        "OneRClassifier": "mlxtend.classifier.oner.OneRClassifier",
        "SequentialFeatureSelector": "mlxtend.feature_selection.sequential_feature_selector.SequentialFeatureSelector",
        "StackingCVClassifier": "mlxtend.classifier.stacking_cv_classification.StackingCVClassifier",
        "StackingCVRegressor": "mlxtend.regressor.stacking_cv_regression.StackingCVRegressor",
        "StackingClassifier": "mlxtend.classifier.stacking_classification.StackingClassifier",
        "StackingRegressor": "mlxtend.regressor.stacking_regression.StackingRegressor",
        "TransactionEncoder": "mlxtend.preprocessing.transactionencoder.TransactionEncoder",
    }

    _type_of_objs = {
        "ColumnSelector": "transformer",
        "CopyTransformer": "transformer",
        "DenseTransformer": "transformer",
        "EnsembleVoteClassifier": "classifier",
        "ExhaustiveFeatureSelector": "transformer",
        "OneRClassifier": "classifier",
        "SequentialFeatureSelector": "transformer",
        "StackingCVClassifier": "classifier",
        "StackingCVRegressor": "regressor",
        "StackingClassifier": "classifier",
        "StackingRegressor": "regressor",
        "TransactionEncoder": "transformer",
    }

    _objs_by_type = {
        "classifier": [
            "EnsembleVoteClassifier",
            "OneRClassifier",
            "StackingCVClassifier",
            "StackingClassifier",
        ],
        "regressor": [
            "StackingCVRegressor",
            "StackingRegressor",
        ],
        "transformer": [
            "ColumnSelector",
            "CopyTransformer",
            "DenseTransformer",
            "ExhaustiveFeatureSelector",
            "SequentialFeatureSelector",
            "TransactionEncoder",
        ],
    }
