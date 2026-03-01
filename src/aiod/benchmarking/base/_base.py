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

    Subclasses must implement ``run()`` which executes the benchmark and
    returns a ``pd.DataFrame`` of results.
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
        heuristic pattern matching

        Parameters
        ----------
        spec : str
            Specification string for the component to add.
        """
        spec = spec.strip()

        if _DATASET_PATTERN.match(spec):
            self._dataset_specs.append(spec)
        elif self._is_resampler(spec):
            self._resampler_specs.append(spec)
        elif _METRIC_PATTERN.match(spec):
            self._metric_specs.append(spec)
        else:
            self._estimator_specs.append(spec)

    @abstractmethod
    def run(self) -> pd.DataFrame:
        """Execute the benchmark and return results.

        Returns
        -------
        pd.DataFrame
            Structured results DataFrame with metrics as index and
            estimator-task combinations as columns.
        """
        ...


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
            Class or function name.
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
        import importlib

        # Try sklearn.metrics first, then builtins
        for module_path in ("sklearn.metrics",):
            try:
                mod = importlib.import_module(module_path)
                fn = getattr(mod, metric_spec, None)
                if fn is not None:
                    return fn
            except ImportError:
                pass

        raise ValueError(
            f"Could not resolve metric '{metric_spec}'. "
            "Ensure it is available in sklearn.metrics."
        )
