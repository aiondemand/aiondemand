"""Sklearn classifiers."""

from aiod.models.apis import _ModelPkgClassifier


class AiodPkg__SklearnClassifiers(_ModelPkgClassifier):
    _tags = {
        "pkg_id": "__multiple",
        "python_dependencies": "scikit-learn",
        "pkg_pypi_name": "scikit-learn",
    }

    # obtained via utils._indexing._preindex_sklearn
    # todo: automate generation
    # todo: include version bounds for availability
    # todo: test generated index against actual index
    _obj_dict = {
        'AdaBoostClassifier': 'sklearn.ensemble._weight_boosting.AdaBoostClassifier',
        'BaggingClassifier': 'sklearn.ensemble._bagging.BaggingClassifier',
        'BernoulliNB': 'sklearn.naive_bayes.BernoulliNB',
        'CalibratedClassifierCV': 'sklearn.calibration.CalibratedClassifierCV',
        'CategoricalNB': 'sklearn.naive_bayes.CategoricalNB',
        'ClassifierChain': 'sklearn.multioutput.ClassifierChain',
        'ComplementNB': 'sklearn.naive_bayes.ComplementNB',
        'DecisionTreeClassifier': 'sklearn.tree._classes.DecisionTreeClassifier',
        'DummyClassifier': 'sklearn.dummy.DummyClassifier',
        'ExtraTreeClassifier': 'sklearn.tree._classes.ExtraTreeClassifier',
        'ExtraTreesClassifier': 'sklearn.ensemble._forest.ExtraTreesClassifier',
        'FixedThresholdClassifier': 'sklearn.model_selection._classification_threshold.FixedThresholdClassifier',
        'GaussianNB': 'sklearn.naive_bayes.GaussianNB',
        'GaussianProcessClassifier': 'sklearn.gaussian_process._gpc.GaussianProcessClassifier',
        'GradientBoostingClassifier': 'sklearn.ensemble._gb.GradientBoostingClassifier',
        'HistGradientBoostingClassifier': 'sklearn.ensemble._hist_gradient_boosting.gradient_boosting.HistGradientBoostingClassifier',
        'KNeighborsClassifier': 'sklearn.neighbors._classification.KNeighborsClassifier',
        'LabelPropagation': 'sklearn.semi_supervised._label_propagation.LabelPropagation',
        'LabelSpreading': 'sklearn.semi_supervised._label_propagation.LabelSpreading',
        'LinearDiscriminantAnalysis': 'sklearn.discriminant_analysis.LinearDiscriminantAnalysis',
        'LinearSVC': 'sklearn.svm._classes.LinearSVC',
        'LogisticRegression': 'sklearn.linear_model._logistic.LogisticRegression',
        'LogisticRegressionCV': 'sklearn.linear_model._logistic.LogisticRegressionCV',
        'MLPClassifier': 'sklearn.neural_network._multilayer_perceptron.MLPClassifier',
        'MultiOutputClassifier': 'sklearn.multioutput.MultiOutputClassifier',
        'MultinomialNB': 'sklearn.naive_bayes.MultinomialNB',
        'NearestCentroid': 'sklearn.neighbors._nearest_centroid.NearestCentroid',
        'NuSVC': 'sklearn.svm._classes.NuSVC',
        'OneVsOneClassifier': 'sklearn.multiclass.OneVsOneClassifier',
        'OneVsRestClassifier': 'sklearn.multiclass.OneVsRestClassifier',
        'OutputCodeClassifier': 'sklearn.multiclass.OutputCodeClassifier',
        'PassiveAggressiveClassifier': 'sklearn.linear_model._passive_aggressive.PassiveAggressiveClassifier',
        'Perceptron': 'sklearn.linear_model._perceptron.Perceptron',
        'QuadraticDiscriminantAnalysis': 'sklearn.discriminant_analysis.QuadraticDiscriminantAnalysis',
        'RadiusNeighborsClassifier': 'sklearn.neighbors._classification.RadiusNeighborsClassifier',
        'RandomForestClassifier': 'sklearn.ensemble._forest.RandomForestClassifier',
        'RidgeClassifier': 'sklearn.linear_model._ridge.RidgeClassifier',
        'RidgeClassifierCV': 'sklearn.linear_model._ridge.RidgeClassifierCV',
        'SGDClassifier': 'sklearn.linear_model._stochastic_gradient.SGDClassifier',
        'SVC': 'sklearn.svm._classes.SVC',
        'SelfTrainingClassifier': 'sklearn.semi_supervised._self_training.SelfTrainingClassifier',
        'StackingClassifier': 'sklearn.ensemble._stacking.StackingClassifier',
        'TunedThresholdClassifierCV': 'sklearn.model_selection._classification_threshold.TunedThresholdClassifierCV',
        'VotingClassifier': 'sklearn.ensemble._voting.VotingClassifier'
    }
