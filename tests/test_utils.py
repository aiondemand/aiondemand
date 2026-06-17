"""
Unit tests for :mod:`aiod.calls.utils`.

These tests validate:
- Response formatting logic (`format_response`)
All tests are pure unit tests and do not require a running backend.
"""

import pandas as pd
import pytest

from aiod.calls.utils import (
    EndpointUndefinedError,
    ServerError,
    format_response,
    wrap_calls,
)

@pytest.mark.parametrize(
    "response,expected_type",
    [
        ({"a": 1}, pd.Series),
        ([{"a": 1}], pd.DataFrame),
    ],
)
def test_format_response_pandas(response, expected_type):
    """
    Verify that requesting 'pandas' format converts:
    - dict  -> pandas.Series
    - list  -> pandas.DataFrame
    """
    result = format_response(response, "pandas")
    assert isinstance(result, expected_type)


@pytest.mark.parametrize(
    "response",
    [
        {"a": 1},
        [{"a": 1}],
    ],
)
def test_format_response_json_passthrough(response):
    """
    Verify that requesting 'json' format returns the input unchanged.
    Ensures the function does not mutate or transform data when
    passthrough behavior is expected.
    """
    result = format_response(response, "json")
    assert result == response


@pytest.mark.parametrize(
    "response,data_format",
    [
        ({"a": 1}, "xml"),
        ("invalid", "pandas"),
        ("invalid", "json"),
    ],
)
def test_format_response_invalid_inputs(response, data_format):
    """
    Verify that unsupported formats or invalid input types raise Exception.
    This ensures that the function raises an error when:
    - Unsupported formats are requested
    - Invalid input types are provided
    """
    with pytest.raises(Exception):
        format_response(response, data_format)
