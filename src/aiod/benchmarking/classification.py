"""Benchmarking for classification estimators."""

__all__ = ["ClassificationBenchmark"]

from collections.abc import Callable
from typing import Any
import pandas as pd

from aiod.benchmarking._benchmarking_dataclasses import (
    FoldResults,
    TaskObject,
)
from aiod.benchmarking.base import BaseBenchmark
from aiod.benchmarking.evaluation import evaluate


class ClassificationBenchmark(BaseBenchmark):
    """Classification benchmark.

    Run a series of classifiers against a series of tasks defined via dataset loaders,
    cross validation splitting strategies and performance metrics, and return results as
    a df (as well as saving to file).
    """

    def __init__(
        self,
        id_format: str | None = None,
        return_data=False,
    ):
        super().__init__()
        self.id_format = id_format
        self.return_data = return_data

    def add_task(
        self,
        dataset_loader: Callable | tuple,
        cv_splitter: Any,
        scorers: list,
        task_id: str | None = None,
        error_score: str = "raise",
    ):
        """Register a classification task to the benchmark."""
        if task_id is None:
            if callable(dataset_loader) and hasattr(dataset_loader, "__name__"):
                dataset_name = dataset_loader.__name__
            elif isinstance(dataset_loader, type):
                dataset_name = dataset_loader.__name__
            else:
                dataset_name = getattr(dataset_loader, "__name__", "_")

            task_id = (
                f"[dataset={dataset_name}]"
                f"_[cv_splitter={cv_splitter.__class__.__name__}]"
            )
        task_kwargs = {
            "data": dataset_loader,
            "cv_splitter": cv_splitter,
            "scorers": scorers,
            "error_score": error_score,
        }
        self._add_task(
            task_id,
            TaskObject(**task_kwargs),
        )

    def _run_validation(self, task: TaskObject, estimator):
        cv_splitter = task.cv_splitter
        scorers = task.scorers
        xy_dict = task.get_y_X("classification")
        
        scores_df = evaluate(
            classifier=estimator,
            cv=cv_splitter,
            scoring=scorers,
            return_data=self.return_data,
            error_score=task.error_score,
            **xy_dict,
        )

        folds = {}
        for ix, row in scores_df.iterrows():
            scores = {}
            for scorer in scorers:
                scores[scorer.__name__] = row["test_" + scorer.__name__]
            scores["fit_time"] = row["fit_time"]
            scores["pred_time"] = row["pred_time"]
            if self.return_data:
                folds[ix] = FoldResults(
                    scores, row["y_test"], row.get("y_pred", None), row.get("y_train", None)
                )
            else:
                folds[ix] = FoldResults(scores)
        return folds
    
    def _format_and_rank_results(self, df: pd.DataFrame) -> pd.DataFrame:
        """misc. formatting for the classification benchmark"""
        if df.empty:
            return df

        if "validation_id" in df.columns:
            df = df.rename(columns={"validation_id": "task_id"})


        # extract metric name from object
        metrics = [getattr(m, "__name__", str(m)) for m in self._metrics]
        for metric in metrics:
            col = f"{metric}_mean"
            if col in df.columns:
                # invert when ranking loss and error metrics
                ascending = "loss" in metric.lower() or "error" in metric.lower()
                df[f"{col}_rank"] = df.groupby("task_id")[col].rank(ascending=ascending, method="min").astype(int)

        final_df = df.T
        final_df.index.name = "Metric / Metadata"

        pd.set_option("display.max_columns", None)
        pd.set_option("display.width", None)

        return final_df