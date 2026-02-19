from aiod.models.apis import _ModelPkgClassifier


class AiodPkg__mlxtend(_ModelPkgClassifier):
    _tags = {
        "pkg_id": "__multiple",
        "python_dependencies": "mlxtend",
        "pkg_pypi_name": "mlxtend",
    }

    _obj_dict = {
        "EnsembleVoteClassifier": "mlxtend.classifier.ensemble_vote.EnsembleVoteClassifier",
        "OneRClassifier": "mlxtend.classifier.oner.OneRClassifier",
        "StackingCVClassifier": "mlxtend.classifier.stacking_cv_classification.StackingCVClassifier",
        "StackingCVRegressor": "mlxtend.regressor.stacking_cv_regression.StackingCVRegressor",
        "StackingClassifier": "mlxtend.classifier.stacking_classification.StackingClassifier",
        "StackingRegressor": "mlxtend.regressor.stacking_regression.StackingRegressor",
    }
