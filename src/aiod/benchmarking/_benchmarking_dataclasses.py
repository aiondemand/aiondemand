"""Dataclasses for benchmarking."""

import copy
from collections.abc import Callable
from dataclasses import dataclass, field, fields
from typing import Any

import numpy as np
import pandas as pd


def _coerce_data_for_evaluate(dataset_loader, task_type=None):
    """Coerce data input object to a dict for evaluation."""
    if callable(dataset_loader) and not hasattr(dataset_loader, "load"):
        # Case 1: Loader function
        data = dataset_loader()

    elif hasattr(dataset_loader, "load"):
        # Case 2: Dataset class or object
        from inspect import isclass

        if isclass(dataset_loader):
            dataset_loader = dataset_loader()

        x = dataset_loader.load("x")
        y = dataset_loader.load("y")

        return {"x": x, "y": y}

    else:
        # Case 3: Data tuple or single data container
        data = dataset_loader

    if isinstance(data, tuple) and len(data) == 2:
        data0 = data[0]
        data1 = data[1]
    elif isinstance(data, tuple) and len(data) == 1:
        data0 = data[0]
        data1 = None
    elif hasattr(data, "data") and hasattr(data, "target"):
        data0 = data.data
        data1 = data.target
    else:
        data0 = data
        data1 = None

    return {"x": data0, "y": data1}


@dataclass
class TaskObject:
    """A benchmarking task."""

    data: Callable | tuple
    cv_splitter: Any
    scorers: list[Any]
    strategy: str = "refit"
    cv_x = None
    cv_global = None
    error_score: str = "raise"
    cv_global_temporal = None

    def get_y_x(self, task_type=None):
        """Get the endogenous and exogenous data."""
        return _coerce_data_for_evaluate(self.data, task_type=task_type)


@dataclass
class FoldResults:
    """Results for a single fold."""
    
    scores: list[dict[str, float | pd.DataFrame]]
    ground_truth: pd.DataFrame | None = None
    predictions: pd.DataFrame | None = None
    train_data: pd.DataFrame | None = None

    def __post_init__(self):
        """Check that scores are in the correct format."""
        for score_name, score_value in self.scores.items():
            if isinstance(score_value, pd.Series):
                self.scores[score_name] = score_value.to_frame()


@dataclass
class ResultObject:
    """Model results for a single task."""

    model_id: str
    task_id: str
    folds: dict[int, FoldResults]
    means: dict[str, float] = field(init=False)
    stds: dict[str, float] = field(init=False)

    def __post_init__(self):
        """Calculate mean and std for each score."""
        self.means = {}
        self.stds = {}
        scores = {}
        for _fold_idx, fold in self.folds.items():
            for score_name, score_value in fold.scores.items():
                if score_name not in scores:
                    scores[score_name] = []
                scores[score_name].append(score_value)
        for name, score in scores.items():
            if all(isinstance(s, (pd.DataFrame, pd.Series)) for s in score):
                score = pd.concat(score, axis=1)
                self.means[name] = np.mean(score, axis=1)
                self.stds[name] = np.std(score, ddof=1, axis=1)
            else:
                self.means[name] = np.mean(score, axis=0)
                self.stds[name] = np.std(score, axis=0, ddof=1)

    def to_dataframe(self):
        """Return results as a pandas DataFrame."""
        result_per_metric = {}
        gts = {}
        preds = {}
        train_data = {}
        for fold_idx, fold in self.folds.items():
            for score_name, score_value in fold.scores.items():
                if score_name not in result_per_metric:
                    result_per_metric[score_name] = {}
                result_per_metric[score_name][f"fold_{fold_idx}_test"] = score_value
            if fold.ground_truth is not None:
                gts[f"ground_truth_fold_{fold_idx}"] = [fold.ground_truth]
            if fold.predictions is not None:
                preds[f"predictions_fold_{fold_idx}"] = [fold.predictions]
            if fold.train_data is not None:
                train_data[f"train_data_fold_{fold_idx}"] = [fold.train_data]
        for metric, mean in self.means.items():
            result_per_metric[metric]["mean"] = mean
        for metric, std in self.stds.items():
            result_per_metric[metric]["std"] = std

        return pd.concat(
            [
                pd.DataFrame(
                    {"validation_id": [self.task_id], "model_id": [self.model_id]}
                ),
                pd.json_normalize(result_per_metric, sep="_"),
                pd.DataFrame(gts),
                pd.DataFrame(preds),
                pd.DataFrame(train_data),
            ],
            axis=1,
        )


def asdict(obj, *, dict_factory=dict, pd_orient="list"):
    """Return the fields of a dataclass as a dict."""
    if not hasattr(type(obj), "__dataclass_fields__"):
        raise TypeError("asdict() should be called on dataclass instances")
    return _asdict_inner(obj, dict_factory, pd_orient)


def _asdict_inner(obj, dict_factory, pd_orient):
    if hasattr(type(obj), "__dataclass_fields__"):
        result = []
        for f in fields(obj):
            value = _asdict_inner(getattr(obj, f.name), dict_factory, pd_orient)
            if f.name == "task_id":
                result.append(("validation_id", value))
            else:
                result.append((f.name, value))
        return dict_factory(result)
    elif isinstance(obj, tuple) and hasattr(obj, "_fields"):
        return type(obj)(*[_asdict_inner(v, dict_factory, pd_orient) for v in obj])
    elif isinstance(obj, (list, tuple)):
        return type(obj)(_asdict_inner(v, dict_factory, pd_orient) for v in obj)
    elif isinstance(obj, dict):
        return type(obj)(
            (
                _asdict_inner(k, dict_factory, pd_orient),
                _asdict_inner(v, dict_factory, pd_orient),
            )
            for k, v in obj.items()
        )
    elif isinstance(obj, pd.Series):
        return obj.to_frame().to_dict(orient=pd_orient)
    elif isinstance(obj, pd.DataFrame):
        return obj.to_dict(orient=pd_orient)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    else:
        return copy.deepcopy(obj)
