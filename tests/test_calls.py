"""Tests for calls module."""

from http import HTTPStatus
from unittest.mock import Mock, patch

import pytest

from aiod.calls.calls import get_asset, get_asset_from_platform


def _mock_response(status_code, json_data):
    """Create a mock response object."""
    response = Mock()
    response.status_code = status_code
    response.json.return_value = json_data
    return response


@patch("aiod.calls.calls.requests.get")
def test_get_asset_404_without_detail_does_not_raise_typeerror(mock_get):
    """Test get_asset does not crash when 404 response lacks 'detail'."""
    mock_get.return_value = _mock_response(HTTPStatus.NOT_FOUND, {})

    result = get_asset("missing_id", asset_type="datasets", data_format="json")

    assert result == {}


@patch("aiod.calls.calls.requests.get")
def test_get_asset_404_with_non_detail_body_does_not_raise_typeerror(mock_get):
    """Test get_asset does not crash when 404 response has no 'detail' key."""
    mock_get.return_value = _mock_response(HTTPStatus.NOT_FOUND, {"error": "not found"})

    result = get_asset("missing_id", asset_type="datasets", data_format="json")

    assert result == {"error": "not found"}


@patch("aiod.calls.calls.requests.get")
def test_get_asset_404_with_detail_still_raises_keyerror(mock_get):
    """Test get_asset still raises KeyError for expected 404 detail response."""
    mock_get.return_value = _mock_response(
        HTTPStatus.NOT_FOUND,
        {"detail": "asset not found"},
    )

    with pytest.raises(KeyError, match="missing_id"):
        get_asset("missing_id", asset_type="datasets", data_format="json")


@patch("aiod.calls.calls.requests.get")
def test_get_asset_from_platform_404_without_detail_does_not_raise_typeerror(mock_get):
    """Test get_asset_from_platform does not crash when 404 lacks 'detail'."""
    mock_get.return_value = _mock_response(HTTPStatus.NOT_FOUND, {})

    result = get_asset_from_platform(
        platform="huggingface",
        platform_identifier="missing_id",
        asset_type="datasets",
        data_format="json",
    )

    assert result == {}