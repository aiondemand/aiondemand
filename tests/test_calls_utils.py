from unittest.mock import Mock

import pandas as pd
import pytest

from aiod.calls.utils import (
    EndpointUndefinedError,
    ServerError,
    format_response,
    wrap_calls,
)


def test_format_response_json():
    # Test valid json formatting for dict
    input_dict = {"key": "value"}
    assert format_response(input_dict, "json") == input_dict

    # Test valid json formatting for list
    input_list = [{"key": "value"}, {"key2": "value2"}]
    assert format_response(input_list, "json") == input_list

def test_format_response_pandas():
    # Test pandas formatting for dict (should return pd.Series)
    input_dict = {"a": 1, "b": 2}
    result_series = format_response(input_dict, "pandas")
    assert isinstance(result_series, pd.Series)
    assert result_series["a"] == 1
    assert result_series["b"] == 2

    # Test pandas formatting for list (should return pd.DataFrame)
    input_list = [{"id": 1, "name": "foo"}, {"id": 2, "name": "bar"}]
    result_df = format_response(input_list, "pandas")
    assert isinstance(result_df, pd.DataFrame)
    assert len(result_df) == 2
    assert "name" in result_df.columns

def test_format_response_invalid():
    # Test unsupported data_format
    with pytest.raises(Exception, match="Format: xml invalid or not supported"):
        format_response({"a": 1}, "xml")

    # Test unsupported response type (e.g. string)
    with pytest.raises(Exception, match="invalid or not supported for responses of"):
        format_response("not a dict or list", "json") # type: ignore

def test_wrap_calls():
    def dummy_func(asset_type, arg1):
        """Fetch ASSET_TYPE with arg1."""
        return f"{asset_type}-{arg1}"

    # wrap_calls takes a list of Callables
    wrapped = wrap_calls("datasets", [dummy_func], "dummy_module")
    
    assert len(wrapped) == 1
    wrapped_func = wrapped[0]
    
    # Test __doc__ replacement
    assert wrapped_func.__doc__ == "Fetch datasets with arg1."
    
    # Test module override
    assert wrapped_func.__module__ == "dummy_module"
    
    # Test partial argument binding
    # asset_type is pre-filled, so we only need to pass arg1
    result = wrapped_func(arg1="test")
    assert result == "datasets-test"

def test_wrap_calls_no_docstring():
    def dummy_func_no_doc(asset_type, arg1):
        return f"{asset_type}-{arg1}"

    wrapped = wrap_calls("datasets", [dummy_func_no_doc], "dummy_module")
    assert wrapped[0].__doc__ == ""

def test_server_error():
    mock_response = Mock()
    mock_response.status_code = 404
    mock_response.json.return_value = {
        "detail": "Resource not found",
        "reference": "REF123"
    }

    error = ServerError(mock_response)
    
    assert error.status_code == 404
    assert error.detail == "Resource not found"
    assert error.reference == "REF123"
    assert error._response == mock_response

def test_endpoint_undefined_error():
    # Simple check to ensure the custom exception can be instantiated properly
    error = EndpointUndefinedError("Undefined")
    assert isinstance(error, Exception)
    assert str(error) == "Undefined"
