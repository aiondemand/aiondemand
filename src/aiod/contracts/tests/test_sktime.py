"""Test validity of sktime API contracts."""

import pytest
from skbase.utils.dependencies import _safe_import

from aiod.contracts.sktime.contracts import (
    aligner,
    classifier,
    clusterer,
    dataset_classification,
    dataset_forecasting,
    dataset_regression,
    detector,
    early_classifier,
    estimator,
    forecaster,
    global_forecaster,
    metric_detection,
    metric_forecasting,
    metric_forecasting_probabilistic,
    network,
    param_est,
    reconciler,
    regressor,
    splitter,
    transformer,
    transformer_pairwise,
    transformer_pairwise_panel,
)
from aiod.contracts.utils import ContractError

AlignerDTW = _safe_import("sktime.alignment.dtw_python.AlignerDTW")
KNeighborsTimeSeriesClassifier = _safe_import(
    "sktime.classification.distance_based.KNeighborsTimeSeriesClassifier"
)
TEASER = _safe_import("sktime.classification.early_classification.TEASER")
TimeSeriesDBSCAN = _safe_import("sktime.clustering.dbscan.TimeSeriesDBSCAN")
Airline = _safe_import("sktime.datasets.Airline")
ACSF1 = _safe_import("sktime.datasets.classification.acsf1.ACSF1")
Tecator = _safe_import("sktime.datasets.regression.tecator.Tecator")
BinarySegmentation = _safe_import("sktime.detection.bs.BinarySegmentation")
InformationGainSegmentation = _safe_import(
    "sktime.detection.igts.InformationGainSegmentation"
)
AggrDist = _safe_import("sktime.dists_kernels.AggrDist")
ScipyDist = _safe_import("sktime.dists_kernels.scipy_dist.ScipyDist")
NaiveForecaster = _safe_import("sktime.forecasting.naive.NaiveForecaster")
TopdownReconciler = _safe_import("sktime.forecasting.reconcile.TopdownReconciler")
TimeMoEForecaster = _safe_import("sktime.forecasting.timemoe.TimeMoEForecaster")
CNNNetwork = _safe_import("sktime.networks.cnn.CNNNetwork")
FixedParams = _safe_import("sktime.param_est.fixed.FixedParams")
DetectionCount = _safe_import(
    "sktime.performance_metrics.detection._count.DetectionCount"
)
MeanAbsolutePercentageError = _safe_import(
    "sktime.performance_metrics.forecasting.MeanAbsolutePercentageError"
)
CRPS = _safe_import(
    "sktime.performance_metrics.forecasting.probabilistic._classes.CRPS"
)
KNeighborsTimeSeriesRegressor = _safe_import(
    "sktime.regression.distance_based.KNeighborsTimeSeriesRegressor"
)
SingleWindowSplitter = _safe_import("sktime.split.SingleWindowSplitter")
BoxCoxTransformer = _safe_import(
    "sktime.transformations.series.boxcox.BoxCoxTransformer"
)


def _generate_cases(obj, contract, expected):
    """Generate variations: class, instance, string, string-instance."""
    if obj is None or "skbase.utils.dependencies" in str(type(obj)):
        return []

    cases = [(obj, contract, expected)]
    if hasattr(obj, "__name__"):
        cases.append((obj.__name__, contract, expected))

    return cases


class BrokenBehaviorForecaster(NaiveForecaster):
    def predict(self, fh=None, X=None):  # noqa: N803
        raise RuntimeError("behavior failure")


class TotallyInvalidDummyClass:
    pass


@pytest.mark.parametrize(
    "obj, contract, expected",
    [
        *_generate_cases(NaiveForecaster, forecaster, True),
        *_generate_cases(KNeighborsTimeSeriesClassifier, classifier, True),
        *_generate_cases(KNeighborsTimeSeriesRegressor, regressor, True),
        *_generate_cases(BoxCoxTransformer, transformer, True),
        *_generate_cases(TimeSeriesDBSCAN, clusterer, True),
        *_generate_cases(AlignerDTW, aligner, True),
        *_generate_cases(BinarySegmentation, detector, True),
        *_generate_cases(SingleWindowSplitter, splitter, True),
        *_generate_cases(CNNNetwork, network, True),
        *_generate_cases(FixedParams, param_est, True),
        *_generate_cases(TEASER, early_classifier, True),
        *_generate_cases(ScipyDist, transformer_pairwise, True),
        *_generate_cases(AggrDist, transformer_pairwise_panel, True),
        *_generate_cases(TimeMoEForecaster, global_forecaster, True),
        *_generate_cases(InformationGainSegmentation, estimator, True),
        *_generate_cases(TopdownReconciler, reconciler, True),
        *_generate_cases(MeanAbsolutePercentageError, metric_forecasting, True),
        *_generate_cases(CRPS, metric_forecasting_probabilistic, True),
        *_generate_cases(DetectionCount, metric_detection, True),
        *_generate_cases(ACSF1, dataset_classification, True),
        *_generate_cases(Airline, dataset_forecasting, True),
        *_generate_cases(Tecator, dataset_regression, True),
        *_generate_cases(NaiveForecaster, classifier, False),
        *_generate_cases(KNeighborsTimeSeriesClassifier, forecaster, False),
        *_generate_cases(BoxCoxTransformer, regressor, False),
    ],
)
def test_istypeof(obj, contract, expected):
    if expected is True:
        assert contract.istypeof(obj, raise_error=True) is True
    else:
        with pytest.raises(ContractError):
            contract.istypeof(obj, raise_error=True)
        assert contract.istypeof(obj) is False

    assert contract.istypeof(TotallyInvalidDummyClass()) is False


@pytest.mark.parametrize(
    "obj,contract,passed,errors",
    [
        (NaiveForecaster, forecaster, True, None),
        (KNeighborsTimeSeriesClassifier, classifier, True, None),
        (BrokenBehaviorForecaster, forecaster, False, "behavior failure"),
    ],
)
def test_runtests(obj, contract, passed, errors):
    """Test runtests behavioral execution."""
    if passed is True:
        result = contract.runtests(obj, raise_error=True)
        assert result["passed"] is True
        assert result["errors"] == []
    else:
        with pytest.raises(Exception, match=errors):
            contract.runtests(obj, raise_error=True)

        result = contract.runtests(obj)
        assert result["passed"] is False
        assert any(errors in e for e in result["errors"])
