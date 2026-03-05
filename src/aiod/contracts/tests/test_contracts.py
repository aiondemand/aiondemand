"""Test validity of arbitrary API contracts."""

import pytest
from sktime.alignment.dtw_python import AlignerDTW
from sktime.classification.distance_based import KNeighborsTimeSeriesClassifier
from sktime.classification.early_classification import TEASER
from sktime.clustering.dbscan import TimeSeriesDBSCAN
from sktime.datasets.classification.acsf1 import ACSF1
from sktime.detection.bs import BinarySegmentation
from sktime.dists_kernels.compose_tab_to_panel import AggrDist
from sktime.forecasting.naive import NaiveForecaster
from sktime.forecasting.reconcile import TopdownReconciler
from sktime.forecasting.timemoe import TimeMoEForecaster
from sktime.networks.cnn import CNNNetwork
from sktime.param_est.fixed import FixedParams
from sktime.performance_metrics.detection._count import DetectionCount
from sktime.performance_metrics.forecasting import MeanAbsolutePercentageError
from sktime.regression.distance_based import KNeighborsTimeSeriesRegressor
from sktime.split import SingleWindowSplitter
from sktime.transformations.series.boxcox import BoxCoxTransformer

from aiod.contracts.base import _BaseContract

# Import the sktime contracts
from aiod.contracts.sktime.contracts import (
    aligner,
    catalogue,
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

ALL_CONTRACTS = [
    forecaster,
    classifier,
    regressor,
    transformer,
    clusterer,
    aligner,
    detector,
    splitter,
    network,
    param_est,
    early_classifier,
    transformer_pairwise,
    transformer_pairwise_panel,
    global_forecaster,
    estimator,
    reconciler,
    metric_forecasting,
    metric_forecasting_probabilistic,
    metric_detection,
    dataset_classification,
    dataset_forecasting,
    dataset_regression,
    catalogue,
]

VALIDATION_PAIRS = [
    (forecaster, NaiveForecaster),
    (classifier, KNeighborsTimeSeriesClassifier),
    (regressor, KNeighborsTimeSeriesRegressor),
    (transformer, BoxCoxTransformer),
    (clusterer, TimeSeriesDBSCAN),
    (aligner, AlignerDTW),
    (detector, BinarySegmentation),
    (splitter, SingleWindowSplitter),
    (network, CNNNetwork),
    (param_est, FixedParams),
    (early_classifier, TEASER),
    (transformer_pairwise, AggrDist),
    (global_forecaster, TimeMoEForecaster),
    (reconciler, TopdownReconciler),
    (metric_forecasting, MeanAbsolutePercentageError),
    (metric_detection, DetectionCount),
    (dataset_classification, ACSF1),
]


class TestArbitraryAPIContracts:
    """Test suite for validating any API Contract."""

    @pytest.mark.parametrize("contract_class", ALL_CONTRACTS)
    def test_contract_inherits_from_base(self, contract_class):
        """Test that the arbitrary contract inherits from _BaseContract."""
        assert issubclass(contract_class, _BaseContract), (
            f"Contract '{contract_class.__name__}' must inherit from _BaseContract "
            "to ensure shared API logic and tag handling."
        )

    @pytest.mark.parametrize("contract_class", ALL_CONTRACTS)
    def test_contract_has_required_tags(self, contract_class):
        """Test that every arbitrary contract has the required metadata."""
        assert hasattr(contract_class, "_tags"), f"""{contract_class.__name__}
        is missing _tags"""
        assert "scitype_name" in contract_class._tags, f"""{contract_class.__name__} 
        missing scitype_name"""
        assert "parent_scitype" in contract_class._tags, f"""{contract_class.__name__} 
        missing parent_scitype"""

    @pytest.mark.parametrize("contract_class", ALL_CONTRACTS)
    def test_check_structure_rejects_invalid_objects(self, contract_class):
        """Test that the contract's _check_structure correctly catches bad inputs."""

        class TotallyInvalidDummyClass:
            pass

        with pytest.raises(TypeError):
            contract_class._check_structure(TotallyInvalidDummyClass)

    @pytest.mark.parametrize("contract_class, valid_model", VALIDATION_PAIRS)
    def test_check_structure_accepts_valid_objects(self, contract_class, valid_model):
        """Test that the contract correctly accepts a model that follows the rules."""
        result = contract_class._check_structure(valid_model)
        assert result is True, f"""{contract_class.__name__} failed to 
        validate {valid_model.__name__}"""
