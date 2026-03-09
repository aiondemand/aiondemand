"""Utilities for evaluating the results of a machine learning experiement."""
import collections.abc
import inspect
import time
import warnings

import numpy as np
import pandas as pd

"""Evaluator class for analyzing results of a machine learning experiment."""
__all__ = ["evaluate"]


     
def _is_proba_classification_score(metric) -> bool:
    PROBA_METRICS = {"brier_score_loss", "log_loss", "roc_auc_score"}
    metric_name = getattr(metric, "__name__", str(metric))
    if metric_name in PROBA_METRICS:
        return True

    if callable(metric):
        sig = inspect.signature(metric)
        params = list(sig.parameters.keys())
        proba_indicators = ["y_proba", "y_pred_proba", "probas_pred", "y_prob"]
        if any(indicator in params for indicator in proba_indicators):
            return True

    try:
        y_true_sample = np.array([0, 1])
        y_pred_proba_sample = np.array([[0.8, 0.2], [0.3, 0.7]])
        metric(y_true_sample, y_pred_proba_sample)
        return True
    except (TypeError, ValueError, AttributeError):
        pass

    return False


def _check_scores(metrics) -> dict:
    if metrics is None:
        from sklearn.metrics import accuracy_score
        metrics = [accuracy_score]

    if not isinstance(metrics, list):
        metrics = [metrics]

    metrics_type = {}

    for metric in metrics:
        if not callable(metric):
            raise ValueError(f"Metric {metric} is not callable")

        scitype = "pred_proba" if _is_proba_classification_score(metric) else "pred"

        if scitype not in metrics_type:
            metrics_type[scitype] = [metric]
        else:
            metrics_type[scitype].append(metric)

        return metrics_type


def _get_column_order_and_datatype(
        metric_types: dict, return_data: bool = True
    ) -> dict:
        y_metadata = {
            "X_train": "object",
            "X_test": "object",
            "y_train": "object",
            "y_test": "object",
        }
        fit_metadata, metrics_metadata = {"fit_time": "float"}, {}
        for scitype in metric_types:
            for metric in metric_types.get(scitype):
                pred_args = _get_pred_args_from_metric(scitype, metric)
                if pred_args == {}:
                    time_key = f"{scitype}_time"
                    result_key = f"test_{metric.__name__}"
                    y_pred_key = f"y_{scitype}"
                else:
                    argval = list(pred_args.values())[0]
                    time_key = f"{scitype}_{argval}_time"
                    result_key = f"test_{metric.__name__}_{argval}"
                    y_pred_key = f"y_{scitype}_{argval}"
                fit_metadata[time_key] = "float"
                metrics_metadata[result_key] = "float"
                if return_data:
                    y_metadata[y_pred_key] = "object"
        if return_data:
            fit_metadata.update(y_metadata)
        metrics_metadata.update(fit_metadata)
        return metrics_metadata.copy()


def _get_pred_args_from_metric(scitype, metric):
        pred_args = {
            "pred_quantiles": "alpha",
        }
        if scitype in pred_args.keys():
            val = getattr(metric, pred_args[scitype], None)
            if val is not None:
                return {pred_args[scitype]: val}
        return {}


def _evaluate_fold(x, meta):
        i, (y_train, y_test, X_train, X_test) = x
        classifier = meta["classifier"]
        scoring = meta["scoring"]
        return_data = meta["return_data"]
        error_score = meta["error_score"]

        score = error_score
        fit_time = np.nan
        pred_time = np.nan
        y_pred = pd.NA
        temp_result = dict()
        y_preds_cache = dict()

        try:
            # fit
            start_fit = time.perf_counter()

            import sklearn
            classifier = sklearn.base.clone(classifier)
            classifier.fit(X=X_train, y=y_train)

            fit_time = time.perf_counter() - start_fit

            # predict based on metrics
            pred_type = {
                "pred_quantiles": "predict_quantiles",
                "pred_proba": "predict_proba",
                "pred": "predict",
            }
            for scitype in scoring:
                method = getattr(classifier, pred_type[scitype])
                for metric in scoring.get(scitype):
                    pred_args = _get_pred_args_from_metric(scitype, metric)
                    if pred_args == {}:
                        time_key = f"{scitype}_time"
                        result_key = f"test_{metric.__name__}"
                        y_pred_key = f"y_{scitype}"
                    else:
                        argval = list(pred_args.values())[0]
                        time_key = f"{scitype}_{argval}_time"
                        result_key = f"test_{metric.__name__}_{argval}"
                        y_pred_key = f"y_{scitype}_{argval}"

                    # make prediction
                    if y_pred_key not in y_preds_cache.keys():
                        start_pred = time.perf_counter()
                        y_pred = method(X_test, **pred_args)
                        pred_time = time.perf_counter() - start_pred
                        temp_result[time_key] = [pred_time]
                        y_preds_cache[y_pred_key] = [y_pred]
                    else:
                        y_pred = y_preds_cache[y_pred_key][0]

                    if scitype == "pred_proba":
                        if "pos_label" in inspect.signature(metric).parameters:
                            pos_label = 1
                            score = metric(y_test, y_pred[:, 1], pos_label=pos_label)
                        else:
                            score = metric(y_test, y_pred)
                    else:
                        score = metric(y_test, y_pred)
                    temp_result[result_key] = [score]

        except Exception as e:
            if error_score == "raise":
                raise e
            else:
                for scitype in scoring:
                    temp_result[f"{scitype}_time"] = [pred_time]
                    if return_data:
                        temp_result[f"y_{scitype}"] = [y_pred]
                    for metric in scoring.get(scitype):
                        temp_result[f"test_{metric.__name__}"] = [score]
                warnings.warn(
                    f"evaluate: fitting of classifier {type(classifier).__name__} failed."
                )

        temp_result["fit_time"] = [fit_time]

        if return_data:
            temp_result["X_train"] = [X_train]
            temp_result["X_test"] = [X_test]
            temp_result["y_train"] = [y_train]
            temp_result["y_test"] = [y_test]
            temp_result.update(y_preds_cache)
        result = pd.DataFrame(temp_result)
        column_order = _get_column_order_and_datatype(scoring, return_data)
        result = result.reindex(columns=column_order.keys())

        return result


def evaluate(
        classifier,
        cv=None,
        X=None,
        y=None,
        scoring: collections.abc.Callable | list[collections.abc.Callable] | None = None,
        return_data: bool = False,
        error_score: str | int | float = np.nan,
    ):
        scoring = _check_scores(scoring)

        if isinstance(cv, int):
            from sklearn.model_selection import KFold
            cv = KFold(n_splits=cv, shuffle=True)
        elif cv is None:
            from sklearn.model_selection import KFold
            cv = KFold(n_splits=3, shuffle=True)

        _evaluate_fold_kwargs = {
            "classifier": classifier,
            "scoring": scoring,
            "return_data": return_data,
            "error_score": error_score,
        }

        def gen_y_X_train_test(y, X, cv):
            # We assume X and y are numpy arrays or pandas dataframes
            for train_instance_idx, test_instance_idx in cv.split(X, y):
                if isinstance(X, pd.DataFrame):
                    X_train = X.iloc[train_instance_idx]
                    X_test = X.iloc[test_instance_idx]
                else:
                    X_train = X[train_instance_idx]
                    X_test = X[test_instance_idx]

                if isinstance(y, (pd.Series, pd.DataFrame)):
                    y_train = y.iloc[train_instance_idx]
                    y_test = y.iloc[test_instance_idx]
                else:
                    y_train = y[train_instance_idx]
                    y_test = y[test_instance_idx]

                yield y_train, y_test, X_train, X_test

        yx_splits = gen_y_X_train_test(y, X, cv)
        
        results = []
        for i, fold_data in enumerate(yx_splits):
            res = _evaluate_fold((i, fold_data), _evaluate_fold_kwargs)
            results.append(res)

        results = pd.concat(results)
        results = results.reset_index(drop=True)

        return results

