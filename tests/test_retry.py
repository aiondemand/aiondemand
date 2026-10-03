"""Tests for the retry logic of SDK HTTP calls."""

from http import HTTPStatus
from unittest import mock

import pytest
import requests

from aiod.calls.utils import _request_with_retry
from aiod.configuration import config


def _mock_response(status_code, headers=None):
    response = mock.Mock(spec=requests.Response)
    response.status_code = status_code
    response.headers = headers or {}
    return response


@pytest.fixture(autouse=True)
def restore_retry_config():
    old_max_retries = config.max_retries
    old_backoff_factor = config.retry_backoff_factor
    yield
    config.max_retries = old_max_retries
    config.retry_backoff_factor = old_backoff_factor


@pytest.fixture
def mock_request():
    with mock.patch("aiod.calls.utils.requests.request") as request:
        yield request


@pytest.fixture
def mock_sleep():
    with mock.patch("aiod.calls.utils.time.sleep") as sleep:
        yield sleep


def test_succeeds_on_first_attempt(mock_request, mock_sleep):
    response = _mock_response(HTTPStatus.OK)
    mock_request.return_value = response

    result = _request_with_retry("get", "http://example.com/")

    assert result is response
    assert mock_request.call_count == 1
    mock_sleep.assert_not_called()


@pytest.mark.parametrize("status", [429, 500, 502, 503, 504])
def test_retries_transient_status_then_succeeds(mock_request, mock_sleep, status):
    mock_request.side_effect = [
        _mock_response(status),
        _mock_response(HTTPStatus.OK),
    ]

    result = _request_with_retry("get", "http://example.com/")

    assert result.status_code == HTTPStatus.OK
    assert mock_request.call_count == 2
    mock_sleep.assert_called_once()


@pytest.mark.parametrize("status", [200, 400, 401, 404])
def test_non_retryable_status_not_retried(mock_request, mock_sleep, status):
    response = _mock_response(status)
    mock_request.return_value = response

    result = _request_with_retry("get", "http://example.com/")

    assert result is response
    assert mock_request.call_count == 1
    mock_sleep.assert_not_called()


def test_returns_last_response_when_retries_exhausted(mock_request, mock_sleep):
    config.max_retries = 2
    last = _mock_response(HTTPStatus.SERVICE_UNAVAILABLE)
    mock_request.side_effect = [
        _mock_response(HTTPStatus.SERVICE_UNAVAILABLE),
        _mock_response(HTTPStatus.BAD_GATEWAY),
        last,
    ]

    result = _request_with_retry("get", "http://example.com/")

    assert result is last
    assert mock_request.call_count == 3
    assert mock_sleep.call_count == 2


def test_max_retries_zero_disables_retries(mock_request, mock_sleep):
    config.max_retries = 0
    response = _mock_response(HTTPStatus.SERVICE_UNAVAILABLE)
    mock_request.return_value = response

    result = _request_with_retry("get", "http://example.com/")

    assert result is response
    assert mock_request.call_count == 1
    mock_sleep.assert_not_called()


def test_honors_retry_after_header(mock_request, mock_sleep):
    mock_request.side_effect = [
        _mock_response(HTTPStatus.TOO_MANY_REQUESTS, headers={"Retry-After": "5"}),
        _mock_response(HTTPStatus.OK),
    ]

    _request_with_retry("get", "http://example.com/")

    mock_sleep.assert_called_once_with(5.0)


def test_exponential_backoff_between_attempts(mock_request, mock_sleep):
    config.max_retries = 3
    config.retry_backoff_factor = 2.0
    mock_request.side_effect = [_mock_response(HTTPStatus.SERVICE_UNAVAILABLE)] * 3 + [
        _mock_response(HTTPStatus.OK)
    ]

    with mock.patch("aiod.calls.utils.random.uniform", return_value=1.0):
        _request_with_retry("get", "http://example.com/")

    assert [call.args[0] for call in mock_sleep.call_args_list] == [2.0, 4.0, 8.0]


def test_retries_on_connection_error(mock_request, mock_sleep):
    mock_request.side_effect = [
        requests.ConnectionError("connection reset"),
        _mock_response(HTTPStatus.OK),
    ]

    result = _request_with_retry("get", "http://example.com/")

    assert result.status_code == HTTPStatus.OK
    assert mock_request.call_count == 2
    mock_sleep.assert_called_once()


def test_raises_connection_error_when_retries_exhausted(mock_request, mock_sleep):
    config.max_retries = 1
    mock_request.side_effect = requests.ConnectionError("connection reset")

    with pytest.raises(requests.ConnectionError):
        _request_with_retry("get", "http://example.com/")

    assert mock_request.call_count == 2
    mock_sleep.assert_called_once()


def test_retries_on_timeout(mock_request, mock_sleep):
    mock_request.side_effect = [
        requests.Timeout("timed out"),
        _mock_response(HTTPStatus.OK),
    ]

    result = _request_with_retry("get", "http://example.com/")

    assert result.status_code == HTTPStatus.OK
    assert mock_request.call_count == 2


def test_passes_method_and_kwargs_to_requests(mock_request, mock_sleep):
    mock_request.return_value = _mock_response(HTTPStatus.OK)

    _request_with_retry("post", "http://example.com/", json={"a": 1}, timeout=10)

    mock_request.assert_called_once_with(
        "post", "http://example.com/", json={"a": 1}, timeout=10
    )
