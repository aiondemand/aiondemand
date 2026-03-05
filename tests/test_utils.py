"""Tests for src/aiod/calls/utils.py."""


import requests
import responses

from aiod.calls.utils import ServerError


@responses.activate
def test_server_error_json_response():
    """ServerError correctly parses detail and reference from a JSON response."""
    responses.post(
        "http://example.com/test",
        json={"detail": "Not found", "reference": "abc123"},
        status=404,
    )
    resp = requests.post("http://example.com/test")

    error = ServerError(resp)

    assert error.status_code == 404
    assert error.detail == "Not found"
    assert error.reference == "abc123"
    assert "404" in str(error)
    assert "Not found" in str(error)


@responses.activate
def test_server_error_non_json_response():
    """ServerError defaults detail and reference to None for non-JSON responses."""
    responses.post(
        "http://example.com/test",
        body=b"<html>Bad Gateway</html>",
        status=502,
        content_type="text/html",
    )
    resp = requests.post("http://example.com/test")

    error = ServerError(resp)

    assert error.status_code == 502
    assert error.detail is None
    assert error.reference is None
    assert "502" in str(error)
    assert isinstance(error, RuntimeError)
