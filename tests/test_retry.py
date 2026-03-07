"""Tests for the automatic retry and rate-limit handling in _request_with_retry."""
import pytest
import requests
import responses
from http import HTTPStatus
from unittest.mock import patch

import aiod
from aiod import config
from aiod.calls.utils import _request_with_retry, ServerError
from aiod.calls.urls import server_url


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_TEST_URL = "http://not.set/not_set/datasets?offset=0&limit=10"


def _add_response(status: int, body: bytes = b'[]', headers: dict | None = None):
    """Register a single mocked response for _TEST_URL."""
    responses.add(
        responses.GET,
        _TEST_URL,
        body=body,
        status=status,
        headers=headers or {},
    )


# ---------------------------------------------------------------------------
# 429 — rate limiting
# ---------------------------------------------------------------------------


@responses.activate
def test_retry_on_429_then_success():
    """A single 429 followed by 200 should succeed after one retry."""
    config.max_retries = 3
    config.retry_backoff_factor = 0  # no sleep in tests
    _add_response(429, headers={"Retry-After": "0"})
    _add_response(200, body=b'[{"resource": "info"}]')

    with patch("time.sleep"):  # prevent actual sleeping
        res = _request_with_retry("GET", _TEST_URL, timeout=5)

    assert res.status_code == HTTPStatus.OK
    assert len(responses.calls) == 2


@responses.activate
def test_retry_on_429_without_retry_after_header():
    """429 without Retry-After header should fall back to exponential backoff."""
    config.max_retries = 2
    config.retry_backoff_factor = 0
    _add_response(429)  # no Retry-After
    _add_response(200, body=b'[]')

    with patch("time.sleep"):
        res = _request_with_retry("GET", _TEST_URL, timeout=5)

    assert res.status_code == HTTPStatus.OK
    assert len(responses.calls) == 2


# ---------------------------------------------------------------------------
# 5xx — server errors
# ---------------------------------------------------------------------------


@responses.activate
def test_retry_on_503_then_success():
    """A single 503 followed by 200 should succeed."""
    config.max_retries = 3
    config.retry_backoff_factor = 0
    _add_response(503)
    _add_response(200, body=b'[]')

    with patch("time.sleep"):
        res = _request_with_retry("GET", _TEST_URL, timeout=5)

    assert res.status_code == HTTPStatus.OK
    assert len(responses.calls) == 2


@responses.activate
def test_retry_on_500_then_success():
    """A 500 should be retried and eventually succeed."""
    config.max_retries = 3
    config.retry_backoff_factor = 0
    _add_response(500)
    _add_response(200, body=b'[]')

    with patch("time.sleep"):
        res = _request_with_retry("GET", _TEST_URL, timeout=5)

    assert res.status_code == HTTPStatus.OK


@responses.activate
def test_retry_exhausted_returns_last_error_response():
    """When all retries are exhausted, the last error response is returned."""
    config.max_retries = 2
    config.retry_backoff_factor = 0
    for _ in range(3):  # 1 initial + 2 retries
        _add_response(503, body=b'{"detail": "Service unavailable"}')

    with patch("time.sleep"):
        res = _request_with_retry("GET", _TEST_URL, timeout=5)

    # Caller is responsible for raising from the response
    assert res.status_code == HTTPStatus.SERVICE_UNAVAILABLE
    assert len(responses.calls) == 3


# ---------------------------------------------------------------------------
# No-retry cases — 4xx (non-429) should not retry
# ---------------------------------------------------------------------------


@responses.activate
def test_no_retry_on_404():
    """404 should be returned immediately with no retries."""
    config.max_retries = 3
    config.retry_backoff_factor = 0
    _add_response(404, body=b'{"detail": "not found"}')

    res = _request_with_retry("GET", _TEST_URL, timeout=5)

    assert res.status_code == HTTPStatus.NOT_FOUND
    assert len(responses.calls) == 1  # no retry


@responses.activate
def test_no_retry_on_400():
    """400 Bad Request should be returned immediately."""
    config.max_retries = 3
    _add_response(400, body=b'{"detail": "bad request"}')

    res = _request_with_retry("GET", _TEST_URL, timeout=5)

    assert res.status_code == HTTPStatus.BAD_REQUEST
    assert len(responses.calls) == 1


# ---------------------------------------------------------------------------
# max_retries = 0 — retry disabled
# ---------------------------------------------------------------------------


@responses.activate
def test_retry_disabled_when_max_retries_zero():
    """When max_retries=0, a 503 should be returned immediately."""
    config.max_retries = 0
    _add_response(503, body=b'{"detail": "unavailable"}')

    res = _request_with_retry("GET", _TEST_URL, timeout=5)

    assert res.status_code == HTTPStatus.SERVICE_UNAVAILABLE
    assert len(responses.calls) == 1  # no retry attempted


# ---------------------------------------------------------------------------
# POST guard
# ---------------------------------------------------------------------------


def test_post_raises_runtime_error():
    """Calling _request_with_retry with POST should raise RuntimeError."""
    config.max_retries = 3
    with pytest.raises(RuntimeError, match="does not support POST"):
        _request_with_retry("POST", _TEST_URL, timeout=5)


def test_patch_raises_runtime_error():
    """Calling _request_with_retry with PATCH should raise RuntimeError."""
    config.max_retries = 3
    with pytest.raises(RuntimeError, match="does not support PATCH"):
        _request_with_retry("PATCH", _TEST_URL, timeout=5)


# ---------------------------------------------------------------------------
# Network exceptions
# ---------------------------------------------------------------------------


@responses.activate
def test_retry_on_connection_error_then_success():
    """A ConnectionError on the first attempt should trigger a retry."""
    config.max_retries = 2
    config.retry_backoff_factor = 0

    responses.add(
        responses.GET,
        _TEST_URL,
        body=requests.ConnectionError("connection reset"),
    )
    _add_response(200, body=b'[]')

    with patch("time.sleep"):
        res = _request_with_retry("GET", _TEST_URL, timeout=5)

    assert res.status_code == HTTPStatus.OK
    assert len(responses.calls) == 2


@responses.activate
def test_retry_on_timeout_then_success():
    """A Timeout on the first attempt should trigger a retry."""
    config.max_retries = 2
    config.retry_backoff_factor = 0

    responses.add(
        responses.GET,
        _TEST_URL,
        body=requests.Timeout("timed out"),
    )
    _add_response(200, body=b'[]')

    with patch("time.sleep"):
        res = _request_with_retry("GET", _TEST_URL, timeout=5)

    assert res.status_code == HTTPStatus.OK
    assert len(responses.calls) == 2


@responses.activate
def test_timeout_all_retries_exhausted_raises():
    """Timeout on every attempt should re-raise the exception after max_retries."""
    config.max_retries = 2
    config.retry_backoff_factor = 0

    for _ in range(3):
        responses.add(
            responses.GET,
            _TEST_URL,
            body=requests.Timeout("timed out"),
        )

    with patch("time.sleep"):
        with pytest.raises(requests.Timeout):
            _request_with_retry("GET", _TEST_URL, timeout=5)

    assert len(responses.calls) == 3


# ---------------------------------------------------------------------------
# Integration — retry surfaced through the public API
# ---------------------------------------------------------------------------


@responses.activate
def test_integration_datasets_get_list_retries_503(setup_test_configuration):
    """Verify retry works end-to-end via the public aiod.datasets.get_list()."""
    config.max_retries = 1
    config.retry_backoff_factor = 0

    responses.add(
        responses.GET,
        f"{server_url()}datasets?offset=0&limit=10",
        status=503,
        json={"detail": "unavailable"},
    )
    responses.add(
        responses.GET,
        f"{server_url()}datasets?offset=0&limit=10",
        status=200,
        body=b'[{"name": "dataset_a"}]',
    )

    with patch("time.sleep"):
        result = aiod.datasets.get_list(data_format="json")

    assert result == [{"name": "dataset_a"}]
    assert len(responses.calls) == 2
