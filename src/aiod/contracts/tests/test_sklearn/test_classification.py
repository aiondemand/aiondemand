import pytest
from skbase.utils.dependencies import _check_soft_dependencies, _safe_import

from aiod.contracts import classifier

LinearRegression = _safe_import(
    import_path="sklearn.ensemble.LinearRegression", pkg_name="scikit-learn"
)

LogisticRegression = _safe_import(
    import_path="sklearn.linear_model.LogisticRegression", pkg_name="scikit-learn"
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


@pytest.mark.skipif(
    not _check_soft_dependencies("scikit-learn", severity="none"),
    reason="run only if scikit-learn is installed",
)
@pytest.mark.parametrize(
    "obj,expected",
    [
        # Regressor -> False
        (LinearRegression, False),
        ("LinearRegression", False),
        (LinearRegression(), False),
        ("LinearRegression()", False),
        # Classifiers -> True
        (LogisticRegression, True),
        ("LogisticRegression", True),
        (LogisticRegression(), True),
        ("LogisticRegression()", True),
        # Trransformers + Classifiers -> True
        (LinearDiscriminantAnalysis, True),
        ("LinearDiscriminantAnalysis", True),
        (LinearDiscriminantAnalysis(), True),
        ("LinearDiscriminantAnalysis()", True),
        # Pipeline class itself -> False
        (Pipeline, False),
        ("Pipeline", False),
        # Pipeline wrapping regressor -> False
        (Pipeline(steps=(("_", LinearRegression()),)), False),
        ("Pipeline(steps=(('_', LinearRegression()),))", False),
        # Pipeline wrapping classifier -> True
        (Pipeline(steps=(("_", LogisticRegression()),)), True),
        ("Pipeline(steps=(('_', LogisticRegression()),))", True),
        # Pipeline wrapping transformers+classifier -> True
        (Pipeline(steps=(("_", LinearDiscriminantAnalysis()),)), True),
        ("Pipeline(steps=(('_', LinearDiscriminantAnalysis()),))", True),
        # GridSearch wrapping regressor -> False
        (
            GridSearchCV(
                estimator=LinearRegression(),
                param_grid={"n_estimators": [50, 100]},
            ),
            False,
        ),
        (
            (
                "GridSearchCV("
                "    estimator=LinearRegression(),"
                "    param_grid={'n_estimators':[50,100]}"
                ")"
            ),
            False,
        ),
        # GridSearch wrapping classifier -> True
        (
            GridSearchCV(
                estimator=LogisticRegression(),
                param_grid={"n_estimators": [50, 100]},
            ),
            True,
        ),
        (
            (
                "GridSearchCV("
                "    estimator=LogisticRegression(),"
                "    param_grid={'n_estimators':[50,100]}"
                ")"
            ),
            True,
        ),
        # GridSearch wrapping transformer+classifier -> True
        (
            GridSearchCV(
                estimator=LinearDiscriminantAnalysis(),
                param_grid={"n_estimators": [50, 100]},
            ),
            True,
        ),
        (
            (
                "GridSearchCV("
                "    estimator=LinearDiscriminantAnalysis(),"
                "    param_grid={'n_estimators':[50,100]}"
                ")"
            ),
            True,
        ),
    ],
)
def test_istypeof(obj, expected):
    assert classifier.istypeof(obj) is expected


@pytest.mark.skipif(
    not _check_soft_dependencies("scikit-learn", severity="none"),
    reason="run only if scikit-learn is installed",
)
def test_runtests_success():
    result = classifier.runtests(LogisticRegression)
    assert result["passed"] is True
    assert result["errors"] == []


@pytest.mark.skipif(
    not _check_soft_dependencies("scikit-learn", severity="none"),
    reason="run only if scikit-learn is installed",
)
def test_runtests_behavior_failure():
    result = classifier.runtests(BrokenBehaviorClassifier)
    assert result["passed"] is False
    assert any("behavior failure" in e for e in result["errors"])
