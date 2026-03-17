"""Automation utilities to update scikit-learn model index entries.

This module compares the generated sklearn estimator registry against the
currently indexed values in ``aiod.models.sklearn_apis.scikit_learn`` and
updates the in-repo index dictionaries.
"""

from __future__ import annotations

import argparse
import ast
import sys
from dataclasses import dataclass
from pathlib import Path
from pprint import pformat

from aiod.utils._indexing._preindex_sklearn import (
    _all_sklearn_estimators_locdict,
    _generate_sklearn_types_of_obj,
)

_MODEL_FILE = (
    Path(__file__).resolve().parents[2] / "models" / "sklearn_apis" / "scikit_learn.py"
)


@dataclass(frozen=True)
class UpdateResult:
    """Summary of model index update operation."""

    added_objects: list[str]
    unknown_types: list[str]
    changed: bool


def _find_assignment_bounds(source: str, variable_name: str) -> tuple[int, int]:
    marker = f"{variable_name} = "
    start = source.find(marker)
    if start == -1:
        raise ValueError(f"Could not find assignment for {variable_name!r}.")

    opening = source.find("{", start)
    if opening == -1:
        raise ValueError(f"Could not find opening dict literal for {variable_name!r}.")

    depth = 0
    in_string = False
    string_char = ""
    escaped = False

    for index in range(opening, len(source)):
        char = source[index]

        if in_string:
            if escaped:
                escaped = False
                continue
            if char == "\\":
                escaped = True
                continue
            if char == string_char:
                in_string = False
                string_char = ""
            continue

        if char in ('"', "'"):
            in_string = True
            string_char = char
            continue

        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                end = index + 1
                while end < len(source) and source[end] in " \t":
                    end += 1
                if end < len(source) and source[end] == "\n":
                    end += 1
                return start, end

    raise ValueError(f"Could not determine end of dict literal for {variable_name!r}.")


def _parse_assignment_dict(source: str, variable_name: str) -> dict:
    start, end = _find_assignment_bounds(source, variable_name)
    assignment_src = source[start:end]
    _, rhs = assignment_src.split("=", maxsplit=1)
    return ast.literal_eval(rhs.strip())


def _format_assignment(variable_name: str, value: dict) -> str:
    formatted = pformat(value, sort_dicts=True, width=88)
    indented = formatted.replace("\n", "\n    ")
    return f"{variable_name} = {indented}\n"


def _replace_assignment(source: str, variable_name: str, value: dict) -> str:
    start, end = _find_assignment_bounds(source, variable_name)
    replacement = _format_assignment(variable_name, value)
    return source[:start] + replacement + source[end:]


def _normalize_type_value(value: str | list[str]) -> str | list[str]:
    if isinstance(value, str):
        return value
    return sorted(set(value))


def _generate_objs_by_type(
    type_of_objs: dict[str, str | list[str]],
) -> dict[str, list[str]]:
    objs_by_type: dict[str, list[str]] = {}
    for obj_name, obj_types in type_of_objs.items():
        normalized_types = [obj_types] if isinstance(obj_types, str) else obj_types
        for obj_type in normalized_types:
            objs_by_type.setdefault(obj_type, []).append(obj_name)
    return objs_by_type


def update_sklearn_index_file(
    *,
    model_file: Path = _MODEL_FILE,
    package_name: str = "sklearn",
    apply_changes: bool = True,
) -> UpdateResult:
    """Update sklearn index dictionaries in scikit_learn model file.

    Parameters
    ----------
    model_file : Path
        Path to the ``scikit_learn.py`` file to update.
    package_name : str, default="sklearn"
        Import name of the package to crawl estimators from.
    apply_changes : bool, default=True
        If True, write updates back to file. If False, only compute diffs.
    """
    source = model_file.read_text(encoding="utf-8")

    existing_obj_dict: dict[str, str] = _parse_assignment_dict(source, "_obj_dict")
    existing_types: dict[str, str | list[str]] = _parse_assignment_dict(
        source, "_type_of_objs"
    )

    discovered_obj_dict = _all_sklearn_estimators_locdict(package_name=package_name)
    discovered_types = _generate_sklearn_types_of_obj(package_name=package_name)

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

    generated_objs_by_type = _generate_objs_by_type(merged_types)
    sorted_objs_by_type = {
        type_name: sorted(set(obj_names))
        for type_name, obj_names in sorted(generated_objs_by_type.items())
    }

    updated = source
    updated = _replace_assignment(
        updated, "_obj_dict", dict(sorted(merged_obj_dict.items()))
    )
    updated = _replace_assignment(
        updated, "_type_of_objs", dict(sorted(merged_types.items()))
    )
    updated = _replace_assignment(updated, "_objs_by_type", sorted_objs_by_type)

    changed = updated != source
    if apply_changes and changed:
        model_file.write_text(updated, encoding="utf-8")

    return UpdateResult(
        added_objects=added_objects,
        unknown_types=sorted(unknown_types),
        changed=changed,
    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Update sklearn estimator index in scikit_learn.py"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check whether index file is up to date without modifying files.",
    )
    parser.add_argument(
        "--package-name",
        default="sklearn",
        help="Import name of package to crawl, defaults to 'sklearn'.",
    )
    parser.add_argument(
        "--model-file",
        default=str(_MODEL_FILE),
        help="Path to scikit_learn.py model file to update.",
    )
    return parser


def main() -> int:
    """Run sklearn index update command-line utility."""
    args = _build_parser().parse_args()

    result = update_sklearn_index_file(
        model_file=Path(args.model_file),
        package_name=args.package_name,
        apply_changes=not args.check,
    )

    mode = "CHECK" if args.check else "APPLY"
    sys.stdout.write(
        f"[{mode}] changed={result.changed} new_objects={len(result.added_objects)}\n"
    )
    if result.added_objects:
        sys.stdout.write("[NEW] " + ", ".join(result.added_objects) + "\n")
    if result.unknown_types:
        sys.stdout.write(
            "[WARN] Missing type mapping for: "
            + ", ".join(result.unknown_types)
            + "\n"
        )

    if args.check and result.changed:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
