"""Registry lookup methods - scikit-learn estimators."""

# adapted from the sktime utility of the same name
# copyright: sktime developers, BSD-3-Clause License (see LICENSE file)
__author__ = ["fkiraly"]
# all_estimators is also based on the sklearn utility of the same name

import inspect


def _all_sklearn_estimators_locdict(package_name="sklearn", serialized=False):
    """Return dictionary of all scikit-learn estimators in sktime and sklearn.

    Parameters
    ----------
    package_name : str, optional (default="sklearn")
        The package from which to retrieve the sklearn estimators.
        This is an import name, e.g., ``"sklearn"``, not a PEP 440 package identifier,
        e.g., ``"scikit-learn"``.

    serialized : bool, optional (default=False)
        If True, returns a serialized version of the dict, via
        ``aiod.utils._inmemory._dict.serialize_dict``.
        If False, returns the dict directly.

    Returns
    -------
    loc_dict : dict
        A dictionary with:

        * keys: str, estimator class name, e.g., ``RandomForestClassifier``
        * values: str, public import path of the estimator, e.g.,
          ``sklearn.ensemble.RandomForestClassifier``
    """
    all_ests = _all_sklearn_estimators(
        package_name=package_name,
        return_names=False,
    )

    def _full_path(est):
        module_name = est.__module__
        public_module_name = module_name.split("._")[0]
        return f"{public_module_name}.{est.__name__}"

    loc_dict = {est.__name__: _full_path(est) for est in all_ests}

    if serialized:
        from aiod.utils._inmemory._dict import serialize_dict

        loc_dict = serialize_dict(loc_dict, name="sklearn_estimators_loc_dict")

    return loc_dict


def _all_sklearn_estimators(
    package_name="sklearn",
    return_names=True,
    as_dataframe=False,
    suppress_import_stdout=True,
):
    """List all scikit-learn objects in a given package.

    This function retrieves all sklearn objects inheriting from ``BaseEstimator``,
    from the import location given by ``package_name``.

    Not included are: the base classes themselves, classes defined in test modules.

    Parameters
    ----------
    package_name : str, optional (default="sklearn")
        The package from which to retrieve the sklearn estimators.
        This is an import name, e.g., ``"sklearn"``, not a PEP 440 package identifier,
        e.g., ``"scikit-learn"``.

    return_names: bool, optional (default=True)

        if True, estimator class name is included in the ``all_estimators``
        return in the order: name, estimator class, optional tags, either as
        a tuple or as pandas.DataFrame columns

        if False, estimator class name is removed from the ``all_estimators`` return.

    as_dataframe: bool, optional (default=False)

        True: ``all_estimators`` will return a ``pandas.DataFrame`` with named
        columns for all of the attributes being returned.

        False: ``all_estimators`` will return a list (either a list of
        estimators or a list of tuples, see Returns)

    suppress_import_stdout : bool, optional. Default=True
        whether to suppress stdout printout upon import.

    Returns
    -------
    all_estimators will return one of the following:

        1. list of estimators, if ``return_names=False``, and ``return_tags`` is None

        2. list of tuples (optional estimator name, class, ~ptional estimator
        tags), if ``return_names=True`` or ``return_tags`` is not ``None``.

        3. ``pandas.DataFrame`` if ``as_dataframe = True``

        if list of estimators:
            entries are estimators matching the query,
            in alphabetical order of estimator name
        if list of tuples:
            list of (optional estimator name, estimator, optional estimator
            tags) matching the query, in alphabetical order of estimator name,
            where
            ``name`` is the estimator name as string, and is an
            optional return
            ``estimator`` is the actual estimator
            ``tags`` are the estimator's values for each tag in return_tags
            and is an optional return.
        if ``DataFrame``:
            column names represent the attributes contained in each column.
            "estimators" will be the name of the column of estimators, "names"
            will be the name of the column of estimator class names and the string(s)
            passed in return_tags will serve as column names for all columns of
            tags that were optionally requested.
    """
    from skbase.lookup import all_objects
    from sklearn.base import BaseEstimator

    MODULES_TO_IGNORE_SKLEARN = [
        "array_api_compat",
        "tests",
        "experimental",
        "conftest",
    ]

    found = all_objects(
        object_types=BaseEstimator,
        package_name=package_name,
        modules_to_ignore=MODULES_TO_IGNORE_SKLEARN,
        as_dataframe=as_dataframe,
        return_names=return_names,
        suppress_import_stdout=suppress_import_stdout,
    )

    result = []
    parent_count = {}
    for name, obj in found:
        for _, other_obj in found:
            if obj in inspect.getmro(other_obj)[1:]:
                parent_count[obj] = parent_count.get(obj, 0) + 1
        if parent_count.get(obj, 0) >= max(2, len(found) // 25):
            if not isinstance(getattr(obj, "_estimator_type", None), str):
                continue
        if obj.__module__.split(".")[0] != package_name:
            continue
        if "Base" in name or "mixin" in name.lower():
            continue
        result.append((name, obj))

    if not return_names:
        return [item[1] for item in result]
    return result


def _generate_sklearn_types_of_obj(package_name) -> dict:
    """
    Generate _type_of_objs dictionary from _all_sklearn_estimators.

    Args:
        type_of_objs: Dictionary mapping object names to their types.

    Returns
    -------
        Dictionary mapping object names to their types (as strings or lists of strings).
    """
    all_est = _all_sklearn_estimators(package_name)
    type_of_objs: dict[str, list[str] | str] = {}

    polymorphic_meta = {
        "classifier",
        "regressor",
        "transformer",
        "clusterer",
        "outlier_detector",
    }

    mixin_to_type = {
        "RegressorMixin": "regressor",
        "ClassifierMixin": "classifier",
        "TransformerMixin": "transformer",
        "ClusterMixin": "clusterer",
        "BiclusterMixin": "biclusterer",
        "DensityMixin": "density",
        "KernelDensity": "density",
        "OutlierMixin": "outlier_detector",
        "_VectorizerMixin": "transformer",
        "SamplerMixin": "sampler",
        "BaseSuccessiveHalving": polymorphic_meta,
        "BaseSearchCV": polymorphic_meta,
        "Pipeline": polymorphic_meta,
        "FrozenEstimator": polymorphic_meta,
    }
    module_type = {
        "manifold": "transformer",
        "covariance": "covariance",
        "feature_selection": "transformer",
        "preprocessing": "transformer",
        "metrics": "metric",
    }
    for est_name, est_class in all_est:
        if package_name not in est_class.__module__:
            continue

        est_type = getattr(est_class, "_estimator_type", None)
        if isinstance(est_type, str) and est_type != "ranker":
            found_types = est_type
        else:
            mro = inspect.getmro(est_class)
            found_types = set()
            for base_class in mro:
                if base_class.__name__ in mixin_to_type:
                    est_type = mixin_to_type[base_class.__name__]
                    if est_type not in found_types:
                        found_types.append(est_type) if isinstance(
                            est_type, str
                        ) else found_types.extend(est_type)

            for module in module_type.keys():
                if module in est_class.__module__ and found_types == []:
                    found_types.append(module_type[module])

        if len(found_types) > 1:
            type_of_objs[est_name] = found_types
        elif len(found_types) == 1:
            type_of_objs[est_name] = found_types[0]

    return type_of_objs
