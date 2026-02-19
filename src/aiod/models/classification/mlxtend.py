from aiod.models.apis import _ModelPkgClassifier


class AiodPkg__mlxtend(_ModelPkgClassifier):
    _tags = {
        "pkg_id": "__multiple",
        "python_dependencies": "mlxtend",
        "pkg_pypi_name": "mlxtend",
    }

    _obj_dict = {
        "ColumnSelector": "mlxtend.feature_selection.column_selector.ColumnSelector",
        "CopyTransformer": "mlxtend.preprocessing.copy_transformer.CopyTransformer",
        "DenseTransformer": "mlxtend.preprocessing.dense_transformer.DenseTransformer",
        "EnsembleVoteClassifier": "mlxtend.classifier.ensemble_vote.EnsembleVoteClassifier",
        "ExhaustiveFeatureSelector": "mlxtend.feature_selection.exhaustive_feature_selector.ExhaustiveFeatureSelector",
        "LabelEncoder": "sklearn.preprocessing.LabelEncoder",
        "LinearRegression": "sklearn.linear_model.LinearRegression",
        "OneRClassifier": "mlxtend.classifier.oner.OneRClassifier",
        "SequentialFeatureSelector": "mlxtend.feature_selection.sequential_feature_selector.SequentialFeatureSelector",
        "StackingCVClassifier": "mlxtend.classifier.stacking_cv_classification.StackingCVClassifier",
        "StackingCVRegressor": "mlxtend.regressor.stacking_cv_regression.StackingCVRegressor",
        "StackingClassifier": "mlxtend.classifier.stacking_classification.StackingClassifier",
        "StackingRegressor": "mlxtend.regressor.stacking_regression.StackingRegressor",
        "TransactionEncoder": "mlxtend.preprocessing.transactionencoder.TransactionEncoder",
    }
