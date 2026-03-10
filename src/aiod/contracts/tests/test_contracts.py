"""Test validity of sktime API contracts."""

import pytest
from sktime.alignment.dtw_python import AlignerDTW
from sktime.classification.distance_based import KNeighborsTimeSeriesClassifier
from sktime.classification.early_classification import TEASER
from sktime.clustering.dbscan import TimeSeriesDBSCAN
from sktime.datasets import Airline
from sktime.datasets.classification.acsf1 import ACSF1
from sktime.datasets.regression.tecator import Tecator
from sktime.detection.bs import BinarySegmentation
from sktime.detection.igts import InformationGainSegmentation
from sktime.dists_kernels import AggrDist
from sktime.dists_kernels.scipy_dist import ScipyDist
from sktime.forecasting.naive import NaiveForecaster
from sktime.forecasting.reconcile import TopdownReconciler
from sktime.forecasting.timemoe import TimeMoEForecaster
from sktime.networks.cnn import CNNNetwork
from sktime.param_est.fixed import FixedParams
from sktime.performance_metrics.detection._count import DetectionCount
from sktime.performance_metrics.forecasting import MeanAbsolutePercentageError
from sktime.performance_metrics.forecasting.probabilistic._classes import CRPS
from sktime.regression.distance_based import KNeighborsTimeSeriesRegressor
from sktime.split import SingleWindowSplitter
from sktime.transformations.series.boxcox import BoxCoxTransformer

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


def _generate_cases(obj, contract, expected):
    """Generate variations: class, instance, string, string-instance."""
    cases = [
        (obj, contract, expected),
        (obj.__name__, contract, expected),
    ]
    try:
        cases.extend(
            [
                (obj(), contract, expected),
                (obj.__name__ + "()", contract, expected),
            ]
        )
    except Exception:
        pass

    return cases


class BrokenBehaviorForecaster(NaiveForecaster):
    def predict(self, fh=None, X=None):  # noqa: N803
        raise RuntimeError("behavior failure")


@pytest.fixture
def invalid_obj():
    class TotallyInvalidDummyClass:
        pass

    return TotallyInvalidDummyClass


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
def test_istypeof(obj, contract, expected, invalid_obj):
    if expected is True:
        assert contract.istypeof(obj, raise_error=True) is True
    else:
        with pytest.raises(ContractError):
            contract.istypeof(obj, raise_error=True)
        assert contract.istypeof(obj) is False

    assert contract.istypeof(invalid_obj) is False


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
