"""Automation utilities to update indexed model libraries."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from aiod.utils._indexing._index_file_utils import (
    _normalize_type_value,
    _parse_assignment_dict,
    _replace_assignment,
)
from aiod.utils._indexing._preindex_external import (
    _all_hyperactive_objects_locdict,
    _all_skpro_estimators_locdict,
    _all_sktime_estimators_locdict,
    _generate_hyperactive_types_of_obj,
    _generate_skpro_types_of_obj,
    _generate_sktime_types_of_obj,
)
from aiod.utils._indexing._preindex_sklearn import (
    _all_sklearn_estimators_locdict,
    _generate_sklearn_types_of_obj,
)

ModelDiscoveryFn = Callable[[str], dict[str, str]]
TypeDiscoveryFn = Callable[[str], dict[str, str | list[str]]]

_BASE_MODEL_DIR = Path(__file__).resolve().parents[2] / "models" / "sklearn_apis"


@dataclass(frozen=True)
class LibraryConfig:
    name: str
    package_name: str
    model_file: Path
    locdict_fn: ModelDiscoveryFn
    type_fn: TypeDiscoveryFn


LIBRARY_CONFIGS: dict[str, LibraryConfig] = {
    "sklearn": LibraryConfig(
        name="sklearn",
        package_name="sklearn",
        model_file=_BASE_MODEL_DIR / "scikit_learn.py",
        locdict_fn=_all_sklearn_estimators_locdict,
        type_fn=_generate_sklearn_types_of_obj,
    ),
    "sktime": LibraryConfig(
        name="sktime",
        package_name="sktime",
        model_file=_BASE_MODEL_DIR / "sktime.py",
        locdict_fn=_all_sktime_estimators_locdict,
        type_fn=_generate_sktime_types_of_obj,
    ),
    "skpro": LibraryConfig(
        name="skpro",
        package_name="skpro",
        model_file=_BASE_MODEL_DIR / "skpro.py",
        locdict_fn=_all_skpro_estimators_locdict,
        type_fn=_generate_skpro_types_of_obj,
    ),
    "hyperactive": LibraryConfig(
        name="hyperactive",
        package_name="hyperactive",
        model_file=_BASE_MODEL_DIR / "hyperactive.py",
        locdict_fn=_all_hyperactive_objects_locdict,
        type_fn=_generate_hyperactive_types_of_obj,
    ),
}


@dataclass(frozen=True)
class LibraryUpdateResult:
    name: str
    changed: bool
    added_objects: list[str]
    unknown_types: list[str]
    skipped: bool
    reason: str | None = None


def _generate_objs_by_type(
    type_of_objs: dict[str, str | list[str]],
) -> dict[str, list[str]]:
    objs_by_type: dict[str, list[str]] = {}
    for obj_name, obj_types in type_of_objs.items():
        normalized_types = [obj_types] if isinstance(obj_types, str) else obj_types
        for obj_type in normalized_types:
            objs_by_type.setdefault(obj_type, []).append(obj_name)
    return {key: sorted(set(value)) for key, value in sorted(objs_by_type.items())}


def update_library_index(
    config: LibraryConfig,
    *,
    apply_changes: bool,
    skip_missing_files: bool,
) -> LibraryUpdateResult:
    model_file = config.model_file
    if not model_file.exists():
        if skip_missing_files:
            return LibraryUpdateResult(
                name=config.name,
                changed=False,
                added_objects=[],
                unknown_types=[],
                skipped=True,
                reason=f"model file not found: {model_file}",
            )
        raise FileNotFoundError(f"Model file not found: {model_file}")

    source = model_file.read_text(encoding="utf-8")
    existing_obj_dict: dict[str, str] = _parse_assignment_dict(source, "_obj_dict")
    existing_types: dict[str, str | list[str]] = _parse_assignment_dict(
        source, "_type_of_objs"
    )

    discovered_obj_dict = config.locdict_fn(config.package_name)
    discovered_types = config.type_fn(config.package_name)

    merged_obj_dict = dict(existing_obj_dict)
    merged_obj_dict.update(discovered_obj_dict)

    added_objects = sorted(set(discovered_obj_dict) - set(existing_obj_dict))

    merged_types: dict[str, str | list[str]] = {}
    unknown_types: list[str] = []
    for obj_name in merged_obj_dict:
        if obj_name in discovered_types:
            merged_types[obj_name] = _normalize_type_value(discovered_types[obj_name])
        elif obj_name in existing_types:
            merged_types[obj_name] = _normalize_type_value(existing_types[obj_name])
        else:
            unknown_types.append(obj_name)

    updated = source
    updated = _replace_assignment(
        updated,
        "_obj_dict",
        dict(sorted(merged_obj_dict.items())),
    )
    updated = _replace_assignment(
        updated,
        "_type_of_objs",
        dict(sorted(merged_types.items())),
    )
    updated = _replace_assignment(
        updated,
        "_objs_by_type",
        _generate_objs_by_type(merged_types),
    )

    changed = updated != source
    if apply_changes and changed:
        model_file.write_text(updated, encoding="utf-8")

    return LibraryUpdateResult(
        name=config.name,
        changed=changed,
        added_objects=added_objects,
        unknown_types=sorted(unknown_types),
        skipped=False,
    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Update indexed model libraries for sklearn APIs.",
    )
    parser.add_argument(
        "--libraries",
        default="sklearn,sktime,skpro,hyperactive",
        help="Comma-separated libraries to update.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Only check for drift without writing files.",
    )
    parser.add_argument(
        "--fail-on-missing-file",
        action="store_true",
        help="Fail if a configured model file is missing.",
    )
    return parser


def main() -> int:
    args = _build_parser().parse_args()
    names = [item.strip() for item in args.libraries.split(",") if item.strip()]

    invalid = [name for name in names if name not in LIBRARY_CONFIGS]
    if invalid:
        raise ValueError(
            "Unknown libraries: "
            + ", ".join(invalid)
            + ". Available: "
            + ", ".join(sorted(LIBRARY_CONFIGS))
        )

    results: list[LibraryUpdateResult] = []
    for name in names:
        config = LIBRARY_CONFIGS[name]
        result = update_library_index(
            config,
            apply_changes=not args.check,
            skip_missing_files=not args.fail_on_missing_file,
        )
        results.append(result)

    has_changes = False
    for result in results:
        if result.skipped:
            sys.stdout.write(f"[{result.name}] skipped: {result.reason}\n")
            continue

        has_changes = has_changes or result.changed
        sys.stdout.write(
            "["
            + result.name
            + "] changed="
            + str(result.changed)
            + " new_objects="
            + str(len(result.added_objects))
            + "\n"
        )
        if result.added_objects:
            sys.stdout.write(
                f"[{result.name}] NEW: {', '.join(result.added_objects)}\n"
            )
        if result.unknown_types:
            sys.stdout.write(
                "["
                + result.name
                + "] WARN missing types: "
                + ", ".join(result.unknown_types)
                + "\n"
            )

    if args.check and has_changes:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
