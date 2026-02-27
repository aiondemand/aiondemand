"""Classification benchmark implementation."""

from __future__ import annotations

import time
from itertools import product
from typing import Any

import numpy as np
import pandas as pd

from aiod.benchmarking.base import _BaseBenchmark

__all__ = ["ClassificationBenchmark"]


class ClassificationBenchmark(_BaseBenchmark):
    """Benchmark for classification estimators.

    Allows registering estimators, dataset loaders, resampling strategies,
    and evaluation metrics via ``add()``, then running all combinations with
    a single ``run()`` call.
    """

    def run(self) -> pd.DataFrame:
        """Execute the benchmark across all registered configurations.

        Returns
        -------
        pd.DataFrame with estimators and metrics as index classes

        Raises
        ------
        ValueError
            If no estimators, datasets, resamplers, or metrics have been
            registered via ``add()``.
        """
        self._validate()

        from aiod.models._registry._craft import craft

        records: list[dict[str, Any]] = []

        for dataset_spec, resampler_spec in product(
            self._dataset_specs, self._resampler_specs
        ):
            dataset_name = self._extract_name(dataset_spec)
            resampler_name = self._extract_name(resampler_spec)
            task_id = f"[dataset={dataset_name}]_[cv={resampler_name}]"

            X, y = craft(dataset_spec)
            cv = craft(resampler_spec)

            # Pre-resolve metric functions
            metric_fns: dict[str, Any] = {
                m: self._resolve_metric(m) for m in self._metric_specs
            }

            for est_spec in self._estimator_specs:
                model_id = self._extract_name(est_spec)
                t_start = time.perf_counter()

                fold_fit_times: list[float] = []
                fold_pred_times: list[float] = []
                fold_scores: dict[str, list[float]] = {m: [] for m in self._metric_specs}

                for X_train, X_test, y_train, y_test in self._split(X, y, cv):
                    # Fresh estimator per fold
                    estimator = craft(est_spec)

                    t0 = time.perf_counter()
                    estimator.fit(X_train, y_train)
                    fit_time = time.perf_counter() - t0
                    fold_fit_times.append(fit_time)

                    t0 = time.perf_counter()
                    y_pred = estimator.predict(X_test)
                    pred_time = time.perf_counter() - t0
                    fold_pred_times.append(pred_time)

                    for metric_name, metric_fn in metric_fns.items():
                        score = metric_fn(y_test, y_pred)
                        fold_scores[metric_name].append(score)

                runtime_secs = time.perf_counter() - t_start

                row: dict[str, Any] = {
                    "task_id": task_id,
                    "model_id": model_id,
                }

                # Per-fold metric scores
                for metric_name, scores in fold_scores.items():
                    for i, score in enumerate(scores):
                        row[f"{metric_name}_fold_{i}_test"] = score
                    row[f"{metric_name}_mean"] = float(np.mean(scores))
                    row[f"{metric_name}_std"] = float(np.std(scores))

                # Per-fold fit times
                for i, ft in enumerate(fold_fit_times):
                    row[f"fit_time_fold_{i}_test"] = ft
                row["fit_time_mean"] = float(np.mean(fold_fit_times))
                row["fit_time_std"] = float(np.std(fold_fit_times))

                # Per-fold prediction times
                for i, pt in enumerate(fold_pred_times):
                    row[f"pred_time_fold_{i}_test"] = pt
                row["pred_time_mean"] = float(np.mean(fold_pred_times))
                row["pred_time_std"] = float(np.std(fold_pred_times))

                row["runtime_secs"] = runtime_secs

                records.append(row)

        df = pd.DataFrame(records)
        df.index.name = None

        # Transpose: metrics become the index, estimator-task combos become columns
        result = df.T
        result.index.name = "Metric / Metadata"

        # Apply display settings for the returned dataframe representation
        pd.set_option("display.max_columns", None)
        pd.set_option("display.max_rows", None)
        pd.set_option("display.width", None)

        return result

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _validate(self) -> None:
        """Raise ValueError if any required component list is empty."""
        missing = []
        if not self._estimator_specs:
            missing.append("estimators")
        if not self._dataset_specs:
            missing.append("dataset loaders")
        if not self._resampler_specs:
            missing.append("resampling strategies")
        if not self._metric_specs:
            missing.append("metrics")
        if missing:
            raise ValueError(
                f"ClassificationBenchmark.run() called with no {', '.join(missing)} "
                "registered. Use add() to register components before running."
            )

    @staticmethod
    def _split(X: Any, y: Any, cv: Any):
        """Yield (X_train, X_test, y_train, y_test) tuples for each fold.

        Parameters
        ----------
        X : array-like
            Feature matrix.
        y : array-like
            Target vector.
        cv : splitter
            A cross-validation splitter with a ``split(X, y)`` method.

        Yields
        ------
        tuple
            ``(X_train, X_test, y_train, y_test)`` for each fold.
        """
        for train_idx, test_idx in cv.split(X, y):
            yield X[train_idx], X[test_idx], y[train_idx], y[test_idx]
