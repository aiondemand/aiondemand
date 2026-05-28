"""Tests for ServerError in aiod.calls.utils."""

import requests
import pytest

from aiod.calls.utils import ServerError


def _make_response(status_code, content, content_type):
    """Helper to create a fake requests.Response."""
    resp = requests.models.Response()
    resp.status_code = status_code
    resp._content = content
    resp.headers["Content-Type"] = content_type
    return resp


class TestServerErrorNonJSON:
    """Tests for ServerError handling of non-JSON responses."""

    def test_non_json_response_does_not_crash(self):
        """ServerError should not raise JSONDecodeError
        when response body is not JSON (e.g., HTML 502)."""
        resp = _make_response(
            status_code=502,
            content=b"<html><body>Bad Gateway</body></html>",
            content_type="text/html",
        )
        # Should not raise any exception
        error = ServerError(resp)
        assert error.status_code == 502

    def test_non_json_response_has_meaningful_message(self):
        """str(error) should contain the status code and
        response body when JSON parsing fails."""
        resp = _make_response(
            status_code=502,
            content=b"<html><body>Bad Gateway</body></html>",
            content_type="text/html",
        )
        error = ServerError(resp)
        error_message = str(error)
        assert "502" in error_message
        assert "Bad Gateway" in error_message

    def test_non_json_response_fields_are_none(self):
        """detail and reference should be None when
        response is not JSON."""
        resp = _make_response(
            status_code=503,
            content=b"Service Unavailable",
            content_type="text/plain",
        )
        error = ServerError(resp)
        assert error.detail is None
        assert error.reference is None

    def test_empty_response_body(self):
        """ServerError should handle empty response bodies."""
        resp = _make_response(
            status_code=500,
            content=b"",
            content_type="text/plain",
        )
        error = ServerError(resp)
        assert error.status_code == 500
        assert error.detail is None


class TestServerErrorJSON:
    """Tests for ServerError handling of JSON responses."""

    def test_json_response_parses_detail(self):
        """detail field should be parsed from JSON body."""
        resp = _make_response(
            status_code=500,
            content=b'{"detail": "Internal Server Error"}',
            content_type="application/json",
        )
        error = ServerError(resp)
        assert error.detail == "Internal Server Error"

    def test_json_response_parses_reference(self):
        """reference field should be parsed from JSON body."""
        resp = _make_response(
            status_code=500,
            content=(
                b'{"detail": "Error occurred",'
                b' "reference": "abc123"}'
            ),
            content_type="application/json",
        )
        error = ServerError(resp)
        assert error.reference == "abc123"

    def test_json_response_preserves_status_code(self):
        """status_code should match the response."""
        resp = _make_response(
            status_code=422,
            content=b'{"detail": "Validation error"}',
            content_type="application/json",
        )
        error = ServerError(resp)
        assert error.status_code == 422

    def test_json_response_has_meaningful_message(self):
        """str(error) should contain the detail from JSON."""
        resp = _make_response(
            status_code=500,
            content=b'{"detail": "Something broke"}',
            content_type="application/json",
        )
        error = ServerError(resp)
        error_message = str(error)
        assert "500" in error_message
        assert "Something broke" in error_message

    def test_json_response_missing_fields(self):
        """detail and reference should be None when
        JSON body lacks those keys."""
        resp = _make_response(
            status_code=400,
            content=b'{"error": "bad request"}',
            content_type="application/json",
        )
        error = ServerError(resp)
        assert error.detail is None
        assert error.reference is None
