"""Base Benchmarking interface."""

import logging
import warnings
from dataclasses import dataclass, field

import pandas as pd
import sklearn
from sklearn.base import BaseEstimator as _BaseEstimator

from aiod.benchmarking._benchmarking_dataclasses import (
    ResultObject,
    TaskObject,
)
from aiod.benchmarking._resolve_obj import _resolve_obj
from aiod.benchmarking._storage_handlers import get_storage_backend


#this would be extended to include some objects that do not wrap BaseEstimator
def _is_initialised_estimator(estimator: _BaseEstimator) -> bool:
    """Check if estimator is initialised BaseEstimator object."""
    if isinstance(estimator, _BaseEstimator):
        return True
    return False

def _check_estimators_type(objs: dict | list | _BaseEstimator) -> None:
    """Check if all estimators are initialised BaseEstimator objects.

    Raises
    ------
    TypeError
        If any of the estimators are not BaseEstimator objects.
    """
    if isinstance(objs, _BaseEstimator):
        objs = [objs]
    items = objs.values() if isinstance(objs, dict) else objs
    compatible = all(_is_initialised_estimator(estimator) for estimator in items)
    if not compatible:
        raise TypeError(
            "One or many estimator(s) is not an initialised BaseEstimator "
            "object(s). Please instantiate the estimator(s) first."
        )


def _coerce_estimator_and_id(estimators, estimator_id=None):
    """Coerce estimators to a dict with estimator_id as key and estimator as value.

    Parameters
    ----------
    estimators : dict, list or BaseEstimator object
        Estimator to coerce to a dict.
    estimator_id : str, optional (default=None)
        Identifier for estimator. If none given then uses estimator's class name.

    Returns
    -------
    estimators : dict
        Dict with estimator_id as key and estimator as value.
    """
    _check_estimators_type(estimators)
    if isinstance(estimators, dict):
        return estimators
    elif isinstance(estimators, list):
        return {estimator.__class__.__name__: estimator for estimator in estimators}
    elif _is_initialised_estimator(estimators):
        estimator_id = estimator_id or estimators.__class__.__name__
        return {estimator_id: estimators}
    else:
        raise TypeError(
            "estimator must be of a type a dict, list or an initialised "
            f"SklearnEstimator object but received {type(estimators)} type."
        )


def _make_strings_unique(strings, new_string):
    """Make string unique by appending _idx if it already exists."""
    if new_string not in strings:
        return new_string
    i = 1
    while f"{new_string}_{i}" in strings:
        i += 1
    return f"{new_string}_{i}"


@dataclass
class _BenchmarkingResults:
    """Results of a benchmarking run."""

    path: str = None
    results: list[ResultObject] = field(default_factory=list)


    def __post_init__(self):
        """Load existing results from path."""
        self.storage_backend =  get_storage_backend(self.path)
        self.results = self.storage_backend(self.path).load()

    def update(self, new_result):
        """Update the results with a new result."""
        self.results.append(new_result)

    def save(self):
        """Save the results to a file."""
        if self.path is not None:
            self.storage_backend(self.path).save(self.results)

    def contains(self, task_id: str, model_id: str):
        """Check if the results contain a specific task and model."""
        return any(
            result.task_id == task_id and result.model_id == model_id
            for result in self.results
        )

    def to_dataframe(self):
        """Convert the results to a pandas DataFrame."""
        if not self.results:
            return pd.DataFrame()
        results_df = [result.to_dataframe() for result in self.results]
        df = pd.concat(results_df, axis=0, ignore_index=True)
        df["runtime_secs"] = df["pred_time_mean"] + df["fit_time_mean"]
        return df


class BaseBenchmark:
    """Base class for benchmarks."""

    def __init__(self):
        self.estimators = {}
        self.tasks = {}


        self._datasets = []
        self._cv_splitters = []
        self._metrics = []

    def add_estimator(
        self,
        estimator: list | dict | _BaseEstimator,
        estimator_id: str | None = None,
    ):
        """Register an estimator to the benchmark.

        Parameters
        ----------
        estimator : dict, list
            Estimator to add to the benchmark.

            * If ``dict``, keys are ``estimator_id``s used to customise identifier ID
              and values are estimators.
            * If ``list``, each element is an estimator. ``estimator_id``s are generated
              automatically using the estimator's class name.

        estimator_id : str, optional (default=None)
            Identifier for estimator. If none given then uses estimator's class name.
        """
        estimators = _coerce_estimator_and_id(estimator, estimator_id)
        for estimator_id, estimator in estimators.items():
            self._add_estimator(estimator, estimator_id)

    def _add_estimator(self, estimator, estimator_id: str):
        """Register a single estimator to the benchmark."""
        #replace with estimator.clone() when implemented in base class
        estimator = sklearn.base.clone(estimator)
        unique_estimator_id = _make_strings_unique(list(self.estimators.keys()), 
                                                    estimator_id)
        if estimator_id != unique_estimator_id:
            warnings.warn(
                message=f"Estimator with ID [id={estimator_id}] already registered, "
                + f"new id is {unique_estimator_id}",
                category=UserWarning,
                stacklevel=2,
            )
        self.estimators[unique_estimator_id] = estimator

    def _add_task(self, task_id: str, task: TaskObject):
        """Register a task to the benchmark."""
        task_id_unique = _make_strings_unique(list(self.tasks.keys()), task_id)
        if task_id != task_id_unique:
            warnings.warn(
                message=f"Task with ID [id={task_id}] already registered, "
                + f"new id is {task_id_unique}",
                category=UserWarning,
                stacklevel=2,
            )
        self.tasks[task_id_unique] = task

    def add(self, spec: str):
        """Add components to the benchmark using spec resolution."""
        obj, obj_type = _resolve_obj(spec)
        
        if obj_type in ("classifier", "regressor"):
            estimators = _coerce_estimator_and_id(obj)
            for estimator_id, estimator in estimators.items():
                self._add_estimator(estimator, estimator_id)
        elif obj_type == "dataset":
            self._datasets.append(obj)
        elif obj_type == "metric":
            self._metrics.append(obj)
        elif obj_type == "cross_validator":
            self._cv_splitters.append(obj)
        else:
            raise TypeError(f"Unrecognized obj_type '{obj_type}' for spec: {spec}")

    def register_stored_tasks(self):
        """Register stored tasks."""
        if self._datasets and self._metrics and self._cv_splitters:
            for dataset_loader in self._datasets:
                if callable(dataset_loader) and hasattr(dataset_loader, "__name__"):
                    dataset_name = dataset_loader.__name__
                elif isinstance(dataset_loader, type):
                    dataset_name = dataset_loader.__name__
                else:
                    dataset_name = getattr(dataset_loader, "__name__", "_")

                for splitter in self._cv_splitters:
                    task_id = (
                        f"[dataset={dataset_name}]"
                        f"_[cv_splitter={splitter.__class__.__name__}]"
                    )

                    task_kwargs = {
                        "data": dataset_loader,
                        "cv_splitter": splitter,
                        "scorers": self._metrics,
                    }
                    self._add_task(
                        task_id,
                        TaskObject(**task_kwargs),
                    )

    def _run(self, results_path: str = None, force_rerun: str = "none"):
        """Run the benchmarking for all tasks and estimators."""
        self.register_stored_tasks()

        results = _BenchmarkingResults(path=results_path)

        for task_id, estimator_id, task, estimator in self._generate_experiments():
            if results.contains(task_id, estimator_id) and (
                force_rerun == "none"
                or (isinstance(force_rerun, list) and estimator_id not in force_rerun)
            ):
                logging.info(
                    f"Skipping validation - model: "
                    f"{task_id} - {estimator_id}"
                    ", as found prior result in results."
                )
                continue

            logging.info(f"Running validation - model: {task_id} - {estimator_id}")
            folds = self._run_validation(task, estimator)
            results.update(
                ResultObject(
                    task_id=task_id,
                    model_id=estimator_id,
                    folds=folds,
                )
            )

        if results_path is not None:
            results.save()
            
        pd.set_option('display.max_columns', None)
        return results.to_dataframe()

    def _generate_experiments(self):
        """Generate experiments for the benchmark."""
        exps = []
        for task_id, task in self.tasks.items():
            for estimator_id, estimator in self.estimators.items():
                exps.append((task_id, estimator_id, task, estimator))
        return exps

    def _format_and_rank_results(self, df: pd.DataFrame) -> pd.DataFrame:
        """To be implemented by benchmark child classes."""
        return df

    def run(self, output_file: str = None, force_rerun: str | list[str] = "none"):
        """Run the benchmarking for all tasks and estimators."""
        df = self._run(output_file, force_rerun)
        return self._format_and_rank_results(df)
