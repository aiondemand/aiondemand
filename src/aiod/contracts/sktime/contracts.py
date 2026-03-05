"""Sktime API contracts."""

from aiod.contracts.sktime._base import _BaseSktimeContract


class dataset_classification(_BaseSktimeContract):  # noqa: N801
    _tags = {
        "scitype_name": "dataset_classification",
        "short_descr": "scitype for sktime classification datasets",
        "parent_scitype": "sktime",
    }

    @classmethod
    def _check_structure(cls, obj: type) -> bool:
        from sktime.datasets.classification._base import BaseClassificationDataset

        super()._check_structure(obj)

        if not issubclass(obj, BaseClassificationDataset):
            raise TypeError("Object is not a sktime BaseClassificationDataset")

        return True


class forecaster(_BaseSktimeContract):  # noqa: N801
    _tags = {
        "scitype_name": "forecaster",
        "short_descr": "scitype for sktime forecasting contract",
        "parent_scitype": "sktime",
    }

    @classmethod
    def _check_structure(cls, obj: type) -> bool:
        from sktime.forecasting.base import BaseForecaster

        super()._check_structure(obj)

        if not issubclass(obj, BaseForecaster):
            raise TypeError("Object is not a sktime BaseForecaster")

        return True


class classifier(_BaseSktimeContract):  # noqa: N801
    _tags = {
        "scitype_name": "classifier",
        "short_descr": "scitype for sktime classification contract",
        "parent_scitype": "sktime",
    }

    @classmethod
    def _check_structure(cls, obj: type) -> bool:
        from sktime.classification.base import BaseClassifier

        super()._check_structure(obj)

        if not issubclass(obj, BaseClassifier):
            raise TypeError("Object is not a sktime BaseClassifier")

        return True


class regressor(_BaseSktimeContract):  # noqa: N801
    _tags = {
        "scitype_name": "regressor",
        "short_descr": "scitype for sktime regression contract",
        "parent_scitype": "sktime",
    }

    @classmethod
    def _check_structure(cls, obj: type) -> bool:
        from sktime.regression.base import BaseRegressor

        super()._check_structure(obj)

        if not issubclass(obj, BaseRegressor):
            raise TypeError("Object is not a sktime BaseRegressor")

        return True


class transformer(_BaseSktimeContract):  # noqa: N801
    _tags = {
        "scitype_name": "transformer",
        "short_descr": "scitype for sktime transformation contract",
        "parent_scitype": "sktime",
    }

    @classmethod
    def _check_structure(cls, obj: type) -> bool:
        from sktime.transformations.base import BaseTransformer

        super()._check_structure(obj)

        if not issubclass(obj, BaseTransformer):
            raise TypeError("Object is not a sktime BaseTransformer")

        return True


class clusterer(_BaseSktimeContract):  # noqa: N801
    _tags = {
        "scitype_name": "clusterer",
        "short_descr": "scitype for sktime clustering contract",
        "parent_scitype": "sktime",
    }

    @classmethod
    def _check_structure(cls, obj: type) -> bool:
        from sktime.clustering.base import BaseClusterer

        super()._check_structure(obj)

        if not issubclass(obj, BaseClusterer):
            raise TypeError("Object is not a sktime BaseClusterer")

        return True


class aligner(_BaseSktimeContract):  # noqa: N801
    _tags = {
        "scitype_name": "aligner",
        "short_descr": "scitype for sktime alignment contract",
        "parent_scitype": "sktime",
    }

    @classmethod
    def _check_structure(cls, obj: type) -> bool:
        from sktime.alignment.base import BaseAligner

        super()._check_structure(obj)

        if not issubclass(obj, BaseAligner):
            raise TypeError("Object is not a sktime BaseAligner")

        return True


class metric_detection(_BaseSktimeContract):  # noqa: N801
    _tags = {
        "scitype_name": "metric_detection",
        "short_descr": "scitype for sktime detection contract",
        "parent_scitype": "sktime",
    }

    @classmethod
    def _check_structure(cls, obj: type) -> bool:
        from sktime.performance_metrics.detection._base import BaseDetectionMetric

        super()._check_structure(obj)

        if not issubclass(obj, BaseDetectionMetric):
            raise TypeError("Object is not a sktime BaseDetectionMetric")

        return True


class detector(_BaseSktimeContract):  # noqa: N801
    _tags = {
        "scitype_name": "detector",
        "short_descr": "scitype for sktime detection contract",
        "parent_scitype": "sktime",
    }

    @classmethod
    def _check_structure(cls, obj: type) -> bool:
        from sktime.detection.base import BaseDetector

        super()._check_structure(obj)

        if not issubclass(obj, BaseDetector):
            raise TypeError("Object is not a sktime BaseDetector")

        return True


class reconciler(_BaseSktimeContract):  # noqa: N801
    _tags = {
        "scitype_name": "reconciler",
        "short_descr": "scitype for sktime reconciliation contract",
        "parent_scitype": "sktime",
    }

    @classmethod
    def _check_structure(cls, obj: type) -> bool:
        from sktime.transformations.hierarchical.reconcile._base import (
            _ReconcilerTransformer,
        )

        super()._check_structure(obj)

        if not issubclass(obj, _ReconcilerTransformer):
            raise TypeError("Object is not a sktime _ReconcilerTransformer")

        return True


class splitter(_BaseSktimeContract):  # noqa: N801
    _tags = {
        "scitype_name": "splitter",
        "short_descr": "scitype for sktime splitters",
        "parent_scitype": "sktime",
    }

    @classmethod
    def _check_structure(cls, obj: type) -> bool:
        from sktime.split.base import BaseSplitter

        super()._check_structure(obj)

        if not issubclass(obj, BaseSplitter):
            raise TypeError("Object is not a sktime BaseSplitter")

        return True


class catalogue(_BaseSktimeContract):  # noqa: N801
    _tags = {
        "scitype_name": "catalogue",
        "short_descr": "scitype for sktime catalogues",
        "parent_scitype": "sktime",
    }

    @classmethod
    def _check_structure(cls, obj: type) -> bool:
        from sktime.catalogues.base import BaseCatalogue

        super()._check_structure(obj)

        if not issubclass(obj, BaseCatalogue):
            raise TypeError("Object is not a sktime BaseCatalogue")

        return True


class network(_BaseSktimeContract):  # noqa: N801
    _tags = {
        "scitype_name": "network",
        "short_descr": "scitype for sktime deep networks",
        "parent_scitype": "sktime",
    }

    @classmethod
    def _check_structure(cls, obj: type) -> bool:
        from sktime.networks.base import BaseDeepNetwork

        super()._check_structure(obj)

        if not issubclass(obj, BaseDeepNetwork):
            raise TypeError("Object is not a sktime BaseDeepNetwork")

        return True


class param_est(_BaseSktimeContract):  # noqa: N801
    _tags = {"scitype_name": "param_est", "parent_scitype": "sktime"}

    @classmethod
    def _check_structure(cls, obj: type) -> bool:
        from sktime.param_est.base import BaseParamFitter

        super()._check_structure(obj)
        if not issubclass(obj, BaseParamFitter):
            raise TypeError("Object is not a sktime BaseParamFitter")
        return True


class metric_forecasting_probabilistic(_BaseSktimeContract):  # noqa: N801
    _tags = {
        "scitype_name": "metric_forecasting_probabilistic",
        "parent_scitype": "sktime",
    }

    @classmethod
    def _check_structure(cls, obj: type) -> bool:
        from sktime.performance_metrics.forecasting.probabilistic._classes import (
            _BaseDistrForecastingMetric,
        )

        super()._check_structure(obj)
        if not issubclass(obj, _BaseDistrForecastingMetric):
            raise TypeError("Object is not a sktime _BaseDistrForecastingMetric")
        return True


class metric_forecasting(_BaseSktimeContract):  # noqa: N801
    _tags = {"scitype_name": "metric_forecasting", "parent_scitype": "sktime"}

    @classmethod
    def _check_structure(cls, obj: type) -> bool:
        from sktime.performance_metrics.forecasting._base import (
            BaseForecastingErrorMetric,
        )

        super()._check_structure(obj)
        if not issubclass(obj, BaseForecastingErrorMetric):
            raise TypeError("Object is not a sktime BaseForecastingErrorMetric")
        return True


class estimator(_BaseSktimeContract):  # noqa: N801
    _tags = {"scitype_name": "estimator", "parent_scitype": "sktime"}

    @classmethod
    def _check_structure(cls, obj: type) -> bool:
        from sktime.base import BaseEstimator

        super()._check_structure(obj)
        if not issubclass(obj, BaseEstimator):
            raise TypeError("Object is not a sktime BaseEstimator")
        return True


class global_forecaster(_BaseSktimeContract):  # noqa: N801
    _tags = {"scitype_name": "global_forecaster", "parent_scitype": "sktime"}

    @classmethod
    def _check_structure(cls, obj: type) -> bool:
        from sktime.forecasting.base import _BaseGlobalForecaster

        super()._check_structure(obj)
        if not issubclass(obj, _BaseGlobalForecaster):
            raise TypeError("Object is not a sktime _BaseGlobalForecaster")
        return True


class early_classifier(_BaseSktimeContract):  # noqa: N801
    _tags = {"scitype_name": "early_classifier", "parent_scitype": "sktime"}

    @classmethod
    def _check_structure(cls, obj: type) -> bool:
        from sktime.classification.early_classification.base import BaseEarlyClassifier

        super()._check_structure(obj)
        if not issubclass(obj, BaseEarlyClassifier):
            raise TypeError("Object is not a sktime BaseEarlyClassifier")
        return True


class transformer_pairwise(_BaseSktimeContract):  # noqa: N801
    _tags = {"scitype_name": "transformer-pairwise", "parent_scitype": "sktime"}

    @classmethod
    def _check_structure(cls, obj: type) -> bool:
        from sktime.dists_kernels.base import BasePairwiseTransformer

        super()._check_structure(obj)
        if not issubclass(obj, BasePairwiseTransformer):
            raise TypeError("Object is not a sktime BasePairwiseTransformer")
        return True


class dataset_forecasting(_BaseSktimeContract):  # noqa: N801
    _tags = {"scitype_name": "dataset_forecasting", "parent_scitype": "sktime"}

    @classmethod
    def _check_structure(cls, obj: type) -> bool:
        from sktime.datasets.forecasting._base import BaseForecastingDataset

        super()._check_structure(obj)
        if not issubclass(obj, BaseForecastingDataset):
            raise TypeError("Object is not a sktime BaseForecastingDataset")
        return True


class transformer_pairwise_panel(_BaseSktimeContract):  # noqa: N801
    _tags = {"scitype_name": "transformer-pairwise-panel", "parent_scitype": "sktime"}

    @classmethod
    def _check_structure(cls, obj: type) -> bool:
        from sktime.dists_kernels.base import BasePairwiseTransformerPanel

        super()._check_structure(obj)
        if not issubclass(obj, BasePairwiseTransformerPanel):
            raise TypeError("Object is not a sktime BasePairwiseTransformerPanel")
        return True


class dataset_regression(_BaseSktimeContract):  # noqa: N801
    _tags = {
        "scitype_name": "dataset_regression",
        "short_descr": "scitype for sktime regression datasets",
        "parent_scitype": "sktime",
    }

    @classmethod
    def _check_structure(cls, obj: type) -> bool:
        from sktime.datasets.regression._base import _RegressionDatasetFromLoader

        super()._check_structure(obj)

        if not issubclass(obj, _RegressionDatasetFromLoader):
            raise TypeError("Object is not a sktime _RegressionDatasetFromLoader")

        return True


__all__ = [
    "dataset_classification",
    "forecaster",
    "classifier",
    "regressor",
    "transformer",
    "clusterer",
    "aligner",
    "metric_detection",
    "detector",
    "reconciler",
    "splitter",
    "catalogue",
    "network",
    "param_est",
    "metric_forecasting_probabilistic",
    "metric_forecasting",
    "estimator",
    "global_forecaster",
    "early_classifier",
    "transformer_pairwise",
    "dataset_forecasting",
    "transformer_pairwise_panel",
    "dataset_regression",
]
