"""Base class for benchmarks."""

from __future__ import annotations

import re
from abc import abstractmethod
from typing import Any

import pandas as pd

__all__ = ["_BaseBenchmark"]

# Patterns used to dispatch add() spec strings to the correct bucket
_DATASET_PATTERN = re.compile(r"^load_\w+\s*\(")
_RESAMPLER_NAMES = {
    "KFold",
    "StratifiedKFold",
    "RepeatedKFold",
    "RepeatedStratifiedKFold",
    "ShuffleSplit",
    "StratifiedShuffleSplit",
    "LeaveOneOut",
    "LeavePOut",
    "GroupKFold",
    "GroupShuffleSplit",
    "TimeSeriesSplit",
}
_METRIC_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")


class _BaseBenchmark:
    """Base class for benchmarks.

    Provides the ``add()`` dispatcher and stores estimator specifications,
    dataset loaders, resampling strategies, and evaluation metrics in
    separate internal lists.
    """

    def __init__(self) -> None:
        """Initialize benchmark with empty component lists."""
        self._estimator_specs: list[str] = []
        self._dataset_specs: list[str] = []
        self._resampler_specs: list[str] = []
        self._metric_specs: list[str] = []


    def add(self, spec: str) -> None:
        """Register a component by its specification string.

        Dispatches the spec to the appropriate internal list based on
        identification via the aiod registry (index classes).

        Parameters
        ----------
        spec : str
            Specification string for the component to add.
        """
        from aiod.models._registry import get
        from aiod.models._registry._cls_lookup import _id_lookup
        from aiod.models._registry._craft import _extract_class_names

        spec = spec.strip()
        name = self._extract_name(spec)

        cls_names = _extract_class_names(spec)
        for cname in cls_names:
            try:
                get(cname)
            except Exception as e:
                raise ValueError(
                    f"Error in Benchmark.add. Component '{cname}' is required "
                    f"to build spec '{spec}', but not found in index class."
                ) from e

            
        lookup = _id_lookup()
        adapter = lookup.get(name)

        if adapter is not None:
            if hasattr(adapter, "_type_of_objs"):
                types = adapter._type_of_objs.get(name, [])
            else:
                try:
                    types = adapter.get_class_tag("object_types", [])
                except Exception:
                    types = []

            if isinstance(types, str):
                types = [types]

            if "dataset" in types:
                self._dataset_specs.append(spec)
                return
            if "resampler" in types:
                self._resampler_specs.append(spec)
                return
            if "metric" in types:
                self._metric_specs.append(spec)
                return

        self._estimator_specs.append(spec)

    @abstractmethod
    def run(self) -> pd.DataFrame:
        """Execute the benchmark and return results.

        Returns a dataframe containing all the results of the experiments including \
        statistical information (means, std) and performance metrics (total runtime, prediction time)
        """

    @staticmethod
    def _is_resampler(spec: str) -> bool:
        """Return True if spec starts with a known resampler class name."""
        # Extract the leading class name (before any "(")
        class_name = spec.split("(")[0].strip()
        return class_name in _RESAMPLER_NAMES

    @staticmethod
    def _extract_name(spec: str) -> str:
        """Extract the base class/function name from a spec string.

        Parameters
        ----------
        spec : str
            Specification string.

        Returns
        -------
        str
            Class or function name (part before the first ``"("``).
        """
        return spec.split("(")[0].strip()

    def _resolve_metric(self, metric_spec: str) -> Any:
        """Import and return a metric function by name.

        Parameters
        ----------
        metric_spec : str
            Bare metric function name, e.g. ``"accuracy_score"``.

        Returns
        -------
        callable
            The metric function.
        """
        from aiod.models._registry import get
        try:
            return get(metric_spec)
        except Exception as e:
            raise ValueError(
                f"Could not resolve metric '{metric_spec}' via index classes. "
            ) from e
