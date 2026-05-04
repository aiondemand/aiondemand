"""Utilities for reading and rewriting model index dictionary assignments."""

from __future__ import annotations

import ast
from pprint import pformat


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