"""Registry lookup methods - scikit-learn estimators."""

# adapted from the sktime utility of the same name
# copyright: sktime developers, BSD-3-Clause License (see LICENSE file)
__author__ = ["fkiraly"]
# all_estimators is also based on the sklearn utility of the same name

import inspect
import re
from pprint import pformat

from skbase.lookup import all_objects


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


def _sklearn_estimators_locdict_by_type(type_filter, serialized=False):
    """Return dictionary of scikit-learn estimators filtered by type.

    Parameters
    ----------
    type_filter : str
        The type of estimator to filter for.
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
    from sklearn.utils import all_estimators

    ests = all_estimators(type_filter=type_filter)
    loc_dict = {name: f"{est.__module__}.{name}" for name, est in ests}
    if serialized:
        from aiod.utils._inmemory._dict import serialize_dict

        loc_dict = serialize_dict(loc_dict, name=f"sklearn_{type_filter}_loc_dict")
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
    from sklearn.base import BaseEstimator

    MODULES_TO_IGNORE_SKLEARN = [
        "array_api_compat",
        "tests",
        "experimental",
        "conftest",
    ]

    return all_objects(
        object_types=BaseEstimator,
        package_name=package_name,
        modules_to_ignore=MODULES_TO_IGNORE_SKLEARN,
        as_dataframe=as_dataframe,
        return_names=return_names,
        suppress_import_stdout=suppress_import_stdout,
    )


def _generate_sklearn_objs_by_type(type_of_objs: dict) -> dict:
    """
    Generate _objs_by_type dictionary from _type_of_objs.

    Args:
        type_of_objs: Dictionary mapping object names to their types.
                     Types can be strings or lists of strings for polymorphic objects.

    Returns
    -------
        Dictionary mapping types to lists of object names.
    """
    objs_by_type: dict[str, list[str]] = {}

    for obj_name, obj_types in type_of_objs.items():
        if isinstance(obj_types, str):
            obj_types = [obj_types]

        for obj_type in obj_types:
            if obj_type not in objs_by_type:
                objs_by_type[obj_type] = []
            objs_by_type[obj_type].append(obj_name)

    return objs_by_type


def _generate_sklearn_types_of_obj() -> dict:
    """
    Generate _type_of_objs dictionary from _all_sklearn_estimators.

    Args:
        type_of_objs: Dictionary mapping object names to their types.

    Returns
    -------
        Dictionary mapping object names to their types (as strings or lists of strings).
    """
    # TODO: handle meta-estimators properly
    all_est = _all_sklearn_estimators()
    type_of_objs: dict[str, list[str] | str] = {}
    mixin_to_type = {
        "RegressorMixin": "regressor",
        "ClassifierMixin": "classifier",
        "TransformerMixin": "transformer",
        "ClusterMixin": "clusterer",
        "BiclusterMixin": "biclusterer",
        "DensityMixin": "density",
        "OutlierMixin": "detector_outlier",
        "_VectorizerMixin": "transformer",
    }

    for est_name, est_class in all_est:
        mro = inspect.getmro(est_class)

        found_types = []
        for base_class in mro:
            if base_class.__name__ in mixin_to_type:
                est_type = mixin_to_type[base_class.__name__]
                if est_type not in found_types:
                    found_types.append(est_type)
        if len(found_types) > 1:
            type_of_objs[est_name] = found_types
        elif len(found_types) == 1:
            type_of_objs[est_name] = found_types[0]

    return type_of_objs


def _sanitize_class_suffix(name: str) -> str:
    """Sanitize string for usage in generated class names."""
    pieces = re.split(r"[^0-9a-zA-Z]+", name)
    return "".join(piece[:1].upper() + piece[1:] for piece in pieces if piece)


def _normalize_object_types(obj_types: str | list[str] | None) -> list[str]:
    """Return object types in normalized list form."""
    if obj_types is None:
        return []
    if isinstance(obj_types, str):
        return [obj_types]
    return list(obj_types)


def generate_sklearn_index_source(
    pypi_package_name="scikit-learn",
    import_root="sklearn",
    class_name=None,
    mode="multiple",
):
    """Generate source code for sklearn index package class(es).

    Parameters
    ----------
    pypi_package_name : str, default="scikit-learn"
        Name of the package in PyPI metadata.
    import_root : str, default="sklearn"
        Import root used to discover sklearn-style estimators.
    class_name : str or None, optional
        Name of class to generate in ``mode='multiple'``.
        If None, this defaults to ``AiodPkg__{ImportRoot}``.
    mode : {"multiple", "single"}, default="multiple"
        If ``"multiple"``, generates one class with ``_obj_dict``, ``_type_of_objs``
        and ``_objs_by_type``.
        If ``"single"``, generates one single-object class per estimator.

    Returns
    -------
    str
        Python source code for generated class definition(s).
    """
    if mode not in {"multiple", "single"}:
        raise ValueError("mode must be one of {'multiple', 'single'}")

    obj_dict = _all_sklearn_estimators_locdict(package_name=import_root)
    type_of_objs = _generate_sklearn_types_of_obj()
    objs_by_type = _generate_sklearn_objs_by_type(type_of_objs)

    lines = [
        '"""Generated sklearn index class(es)."""',
        "",
        "from aiod.models.apis import _ModelPkgSklearnEstimator",
        "",
        "",
    ]

    if mode == "multiple":
        if class_name is None:
            class_name = f"AiodPkg__{_sanitize_class_suffix(import_root)}"

        object_types = sorted(objs_by_type.keys())

        lines.extend(
            [
                f"class {class_name}(_ModelPkgSklearnEstimator):",
                "    _tags = {",
                '        "pkg_id": "__multiple",',
                f'        "python_dependencies": "{pypi_package_name}",',
                f'        "pkg_pypi_name": "{pypi_package_name}",',
                f"        \"object_types\": {pformat(object_types)},",
                "    }",
                "",
                f"    _obj_dict = {pformat(obj_dict, sort_dicts=True)}",
                "",
                f"    _type_of_objs = {pformat(type_of_objs, sort_dicts=True)}",
                "",
                f"    _objs_by_type = {pformat(objs_by_type, sort_dicts=True)}",
                "",
            ]
        )
        return "\n".join(lines)

    for estimator_name in sorted(obj_dict):
        estimator_class_name = f"AiodPkg__{_sanitize_class_suffix(estimator_name)}"
        estimator_obj_types = _normalize_object_types(type_of_objs.get(estimator_name))
        lines.extend(
            [
                f"class {estimator_class_name}(_ModelPkgSklearnEstimator):",
                "    _tags = {",
                f'        "pkg_id": "{estimator_name}",',
                f'        "python_dependencies": "{pypi_package_name}",',
                f'        "pkg_pypi_name": "{pypi_package_name}",',
                f"        \"object_types\": {pformat(estimator_obj_types)},",
                "    }",
                "",
                f'    _obj = "{obj_dict[estimator_name]}"',
                "",
                "",
            ]
        )

    return "\n".join(lines).rstrip() + "\n"
