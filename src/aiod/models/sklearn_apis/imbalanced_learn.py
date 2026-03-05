# ruff: noqa: E501
"""imbalanced-learn model package."""

from aiod.models.apis import _ModelPkgSklearnEstimator


class AiodPkg__ImbalancedLearn(_ModelPkgSklearnEstimator):
    _tags = {
        "pkg_id": "__multiple",
        "python_dependencies": "imbalanced-learn",
        "pkg_pypi_name": "imbalanced-learn",
        "object_types": ["classifier", "sampler"],
    }

    _obj_dict = {
        "ADASYN": "imblearn.over_sampling.ADASYN",
        "AllKNN": "imblearn.under_sampling.AllKNN",
        "BalancedBaggingClassifier": "imblearn.ensemble.BalancedBaggingClassifier",
        "BalancedRandomForestClassifier": "imblearn.ensemble.BalancedRandomForestClassifier",
        "BorderlineSMOTE": "imblearn.over_sampling.BorderlineSMOTE",
        "ClusterCentroids": "imblearn.under_sampling.ClusterCentroids",
        "CondensedNearestNeighbour": "imblearn.under_sampling.CondensedNearestNeighbour",
        "EasyEnsembleClassifier": "imblearn.ensemble.EasyEnsembleClassifier",
        "EditedNearestNeighbours": "imblearn.under_sampling.EditedNearestNeighbours",
        "FunctionSampler": "imblearn.base.FunctionSampler",
        "InstanceHardnessThreshold": "imblearn.under_sampling.InstanceHardnessThreshold",
        "KMeansSMOTE": "imblearn.over_sampling.KMeansSMOTE",
        "NearMiss": "imblearn.under_sampling.NearMiss",
        "NeighbourhoodCleaningRule": "imblearn.under_sampling.NeighbourhoodCleaningRule",
        "OneSidedSelection": "imblearn.under_sampling.OneSidedSelection",
        "RUSBoostClassifier": "imblearn.ensemble.RUSBoostClassifier",
        "RandomOverSampler": "imblearn.over_sampling.RandomOverSampler",
        "RandomUnderSampler": "imblearn.under_sampling.RandomUnderSampler",
        "RepeatedEditedNearestNeighbours": "imblearn.under_sampling.RepeatedEditedNearestNeighbours",
        "SMOTE": "imblearn.over_sampling.SMOTE",
        "SMOTEENN": "imblearn.combine.SMOTEENN",
        "SMOTEN": "imblearn.over_sampling.SMOTEN",
        "SMOTENC": "imblearn.over_sampling.SMOTENC",
        "SMOTETomek": "imblearn.combine.SMOTETomek",
        "SVMSMOTE": "imblearn.over_sampling.SVMSMOTE",
        "TomekLinks": "imblearn.under_sampling.TomekLinks",
    }

    _type_of_objs = {
        "ADASYN": "sampler",
        "AllKNN": "sampler",
        "BalancedBaggingClassifier": "classifier",
        "BalancedRandomForestClassifier": "classifier",
        "BorderlineSMOTE": "sampler",
        "ClusterCentroids": "sampler",
        "CondensedNearestNeighbour": "sampler",
        "EasyEnsembleClassifier": "classifier",
        "EditedNearestNeighbours": "sampler",
        "FunctionSampler": "sampler",
        "InstanceHardnessThreshold": "sampler",
        "KMeansSMOTE": "sampler",
        "NearMiss": "sampler",
        "NeighbourhoodCleaningRule": "sampler",
        "OneSidedSelection": "sampler",
        "RUSBoostClassifier": "classifier",
        "RandomOverSampler": "sampler",
        "RandomUnderSampler": "sampler",
        "RepeatedEditedNearestNeighbours": "sampler",
        "SMOTE": "sampler",
        "SMOTEENN": "sampler",
        "SMOTEN": "sampler",
        "SMOTENC": "sampler",
        "SMOTETomek": "sampler",
        "SVMSMOTE": "sampler",
        "TomekLinks": "sampler",
    }

    _objs_by_type = {
        "classifier": [
            "BalancedBaggingClassifier",
            "BalancedRandomForestClassifier",
            "EasyEnsembleClassifier",
            "RUSBoostClassifier",
        ],
        "sampler": [
            "ADASYN",
            "AllKNN",
            "BorderlineSMOTE",
            "ClusterCentroids",
            "CondensedNearestNeighbour",
            "EditedNearestNeighbours",
            "FunctionSampler",
            "InstanceHardnessThreshold",
            "KMeansSMOTE",
            "NearMiss",
            "NeighbourhoodCleaningRule",
            "OneSidedSelection",
            "RandomOverSampler",
            "RandomUnderSampler",
            "RepeatedEditedNearestNeighbours",
            "SMOTE",
            "SMOTEENN",
            "SMOTEN",
            "SMOTENC",
            "SMOTETomek",
            "SVMSMOTE",
            "TomekLinks",
        ],
    }
