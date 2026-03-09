import pytest
from skbase.utils.dependencies import _check_soft_dependencies, _safe_import

from aiod.contracts.sklearn import (
    biclusterer,
    classifier,
    clusterer,
    density,
    estimator,
    outlier_detector,
    regressor,
    transformer,
)

LinearRegression = _safe_import(
    import_path="sklearn.linear_model.LinearRegression", pkg_name="scikit-learn"
)

LogisticRegression = _safe_import(
    import_path="sklearn.linear_model.LogisticRegression", pkg_name="scikit-learn"
)

AdditiveChi2Sampler = _safe_import(
    import_path="sklearn.kernel_approximation.AdditiveChi2Sampler",
    pkg_name="scikit-learn",
)

AffinityPropagation = _safe_import(
    import_path="sklearn.cluster.AffinityPropagation", pkg_name="scikit-learn"
)

SpectralBiclustering = _safe_import(
    import_path="sklearn.cluster.SpectralBiclustering", pkg_name="scikit-learn"
)

BayesianGaussianMixture = _safe_import(
    import_path="sklearn.mixture.BayesianGaussianMixture", pkg_name="scikit-learn"
)

EllipticEnvelope = _safe_import(
    import_path="sklearn.covariance.EllipticEnvelope", pkg_name="scikit-learn"
)

Birch = _safe_import(import_path="sklearn.cluster.Birch", pkg_name="scikit-learn")

PLSRegression = _safe_import(
    import_path="sklearn.cross_decomposition.PLSRegression", pkg_name="scikit-learn"
)

LinearDiscriminantAnalysis = _safe_import(
    import_path="sklearn.discriminant_analysis.LinearDiscriminantAnalysis",
    pkg_name="scikit-learn",
)

Pipeline = _safe_import(
    import_path="sklearn.pipeline.Pipeline", pkg_name="scikit-learn"
)

GridSearchCV = _safe_import(
    import_path="sklearn.model_selection.GridSearchCV", pkg_name="scikit-learn"
)


class BrokenBehaviorClassifier(LogisticRegression):
    def predict(self, X):  # noqa: N803
        raise RuntimeError("behavior failure")


def _generate_cases(obj, *args):
    return [
        (obj, *args),
        (obj(), *args),
        (obj.__name__, *args),
        (obj.__name__ + "()", *args),
        (Pipeline(steps=(("_", obj()),)), *args),
        (f"Pipeline(steps=(('_', {obj.__name__}()),))", *args),
        (
            GridSearchCV(
                estimator=obj(),
                param_grid={"n_estimators": [50, 100]},
            ),
            *args,
        ),
        (
            (
                "GridSearchCV("
                f"    estimator={obj.__name__}(),"
                "    param_grid={'n_estimators': [50, 100]},"
                ")"
            ),
            *args,
        ),
    ]


@pytest.mark.skipif(
    not _check_soft_dependencies("scikit-learn", severity="none"),
    reason="run only if scikit-learn is installed",
)
@pytest.mark.parametrize(
    "obj,contract,expected",
    [
        *_generate_cases(LinearRegression, estimator, True),
        *_generate_cases(LinearRegression, regressor, True),
        *_generate_cases(PLSRegression, regressor, True),
        *_generate_cases(LogisticRegression, regressor, False),
        *_generate_cases(LogisticRegression, classifier, True),
        *_generate_cases(LinearDiscriminantAnalysis, classifier, True),
        *_generate_cases(LinearRegression, classifier, False),
        *_generate_cases(AdditiveChi2Sampler, transformer, True),
        *_generate_cases(LinearDiscriminantAnalysis, transformer, True),
        *_generate_cases(LinearRegression, transformer, False),
        *_generate_cases(AffinityPropagation, clusterer, True),
        *_generate_cases(Birch, clusterer, True),
        *_generate_cases(LinearRegression, clusterer, False),
        *_generate_cases(SpectralBiclustering, biclusterer, True),
        *_generate_cases(LinearRegression, biclusterer, False),
        *_generate_cases(BayesianGaussianMixture, density, True),
        *_generate_cases(LinearRegression, density, False),
        *_generate_cases(EllipticEnvelope, outlier_detector, True),
        *_generate_cases(LinearRegression, outlier_detector, False),
        (Pipeline, estimator, True),
        (GridSearchCV, classifier, False),
        ("Pipeline", classifier, False),
        ("GridSearchCV", estimator, True),
    ],
)
def test_istypeof(obj, contract, expected):
    assert contract.istypeof(obj) is expected


@pytest.mark.skipif(
    not _check_soft_dependencies("scikit-learn", severity="none"),
    reason="run only if scikit-learn is installed",
)
@pytest.mark.parametrize(
    "obj,contract,passed,errors",
    [
        (LogisticRegression, classifier, True, None),
        (BrokenBehaviorClassifier, classifier, False, "behavior failure"),
    ],
)
def test_runtests(obj, contract, passed, errors):
    result = contract.runtests(obj)
    assert result["passed"] is passed
    if passed:
        assert result["errors"] == []
    else:
        assert any(errors in e for e in result["errors"])
