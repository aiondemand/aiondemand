"""Preindex helpers for non-sklearn packages."""

from __future__ import annotations

import importlib
import inspect
import pkgutil
from typing import Any


def _all_skbase_objects_with_names(package_name: str) -> list[tuple[str, type]]:
    from skbase.base import BaseObject
    from skbase.lookup import all_objects

    found = all_objects(
        object_types=BaseObject,
        package_name=package_name,
        return_names=True,
        suppress_import_stdout=True,
    )
    return [
        (name, obj)
        for name, obj in found
        if getattr(obj, "__module__", "").split(".")[0] == package_name
    ]


def _all_skbase_objects_locdict(package_name: str) -> dict[str, str]:
    def _full_path(estimator: type) -> str:
        module_name = estimator.__module__
        public_module_name = module_name.split("._")[0]
        return f"{public_module_name}.{estimator.__name__}"

    objects = _all_skbase_objects_with_names(package_name)
    return {name: _full_path(obj) for name, obj in objects}


def _all_registry_objects_with_names(
    package_name: str,
    registry_module_name: str,
) -> list[tuple[str, type]]:
    try:
        registry_module = importlib.import_module(registry_module_name)
    except Exception:
        return []

    all_estimators = getattr(registry_module, "all_estimators", None)
    if not callable(all_estimators):
        return []

    try:
        found = all_estimators(return_names=True)
    except TypeError:
        try:
            found = all_estimators(as_dataframe=False, return_names=True)
        except Exception:
            return []
    except Exception:
        return []

    return [
        (name, obj)
        for name, obj in found
        if getattr(obj, "__module__", "").split(".")[0] == package_name
    ]


def _normalize_type_tag(tag_value: Any) -> str | list[str] | None:
    if tag_value is None:
        return None
    if isinstance(tag_value, str):
        return tag_value
    if isinstance(tag_value, (tuple, list, set)):
        normalized = sorted({str(item) for item in tag_value if item is not None})
        if not normalized:
            return None
        if len(normalized) == 1:
            return normalized[0]
        return normalized
    return str(tag_value)


def _extract_skbase_object_type(obj: type) -> str | list[str] | None:
    tag_keys = [
        "object_type",
        "object_types",
        "scitype",
        "scitype:y",
        "task",
    ]

    for key in tag_keys:
        if hasattr(obj, "get_class_tag"):
            try:
                value = obj.get_class_tag(key, raise_error=False)
            except TypeError:
                value = obj.get_class_tag(key)
            normalized = _normalize_type_tag(value)
            if normalized is not None:
                return normalized

    module_parts = obj.__module__.split(".")
    if len(module_parts) > 1:
        module_hint = module_parts[1]
        module_map = {
            "forecasting": "forecaster",
            "classification": "classifier",
            "regression": "regressor",
            "transformations": "transformer",
            "detection": "detector",
            "metrics": "metric",
        }
        if module_hint in module_map:
            return module_map[module_hint]
    return None


def _generate_skbase_types_of_obj(package_name: str) -> dict[str, str | list[str]]:
    objects = _all_skbase_objects_with_names(package_name)
    type_of_objs: dict[str, str | list[str]] = {}
    for name, obj in objects:
        obj_type = _extract_skbase_object_type(obj)
        if obj_type is not None:
            type_of_objs[name] = obj_type
    return type_of_objs


def _all_sktime_estimators_locdict(package_name: str = "sktime") -> dict[str, str]:
    objects = _all_registry_objects_with_names(
        package_name=package_name,
        registry_module_name=f"{package_name}.registry",
    )
    if not objects:
        return _all_skbase_objects_locdict(package_name=package_name)
    return {
        name: f"{obj.__module__.split('._')[0]}.{obj.__name__}" for name, obj in objects
    }


def _generate_sktime_types_of_obj(
    package_name: str = "sktime",
) -> dict[str, str | list[str]]:
    objects = _all_registry_objects_with_names(
        package_name=package_name,
        registry_module_name=f"{package_name}.registry",
    )
    if objects:
        type_of_objs: dict[str, str | list[str]] = {}
        for name, obj in objects:
            obj_type = _extract_skbase_object_type(obj)
            if obj_type is not None:
                type_of_objs[name] = obj_type
        if type_of_objs:
            return type_of_objs
    return _generate_skbase_types_of_obj(package_name=package_name)


def _all_skpro_estimators_locdict(package_name: str = "skpro") -> dict[str, str]:
    objects = _all_registry_objects_with_names(
        package_name=package_name,
        registry_module_name=f"{package_name}.registry",
    )
    if not objects:
        return _all_skbase_objects_locdict(package_name=package_name)
    return {
        name: f"{obj.__module__.split('._')[0]}.{obj.__name__}" for name, obj in objects
    }


def _generate_skpro_types_of_obj(
    package_name: str = "skpro",
) -> dict[str, str | list[str]]:
    objects = _all_registry_objects_with_names(
        package_name=package_name,
        registry_module_name=f"{package_name}.registry",
    )
    if objects:
        type_of_objs: dict[str, str | list[str]] = {}
        for name, obj in objects:
            obj_type = _extract_skbase_object_type(obj)
            if obj_type is not None:
                type_of_objs[name] = obj_type
        if type_of_objs:
            return type_of_objs
    return _generate_skbase_types_of_obj(package_name=package_name)


def _all_hyperactive_objects_locdict(
    package_name: str = "hyperactive",
) -> dict[str, str]:
    if package_name != "hyperactive":
        raise ValueError("Hyperactive indexer expects package_name='hyperactive'.")

    gfo_pkg = importlib.import_module("hyperactive.opt.gfo")
    objects: dict[str, str] = {}

    for _, module_name, _ in pkgutil.walk_packages(
        gfo_pkg.__path__,
        prefix=f"{gfo_pkg.__name__}.",
    ):
        module = importlib.import_module(module_name)
        for class_name, cls in inspect.getmembers(module, inspect.isclass):
            if cls.__module__ != module.__name__:
                continue
            if class_name.startswith("_"):
                continue
            objects[class_name] = f"{module.__name__}.{class_name}"

    return dict(sorted(objects.items()))


def _generate_hyperactive_types_of_obj(
    package_name: str = "hyperactive",
) -> dict[str, str]:
    locdict = _all_hyperactive_objects_locdict(package_name=package_name)
    return dict.fromkeys(locdict, "optimizer")
