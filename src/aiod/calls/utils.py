import random
import time
from collections.abc import Callable
from functools import partial, update_wrapper
from http import HTTPStatus
from typing import Literal

import pandas as pd
import requests

from aiod.configuration import config

_RETRYABLE_STATUS_CODES = frozenset(
    {
        HTTPStatus.TOO_MANY_REQUESTS,
        HTTPStatus.INTERNAL_SERVER_ERROR,
        HTTPStatus.BAD_GATEWAY,
        HTTPStatus.SERVICE_UNAVAILABLE,
        HTTPStatus.GATEWAY_TIMEOUT,
    }
)


def _request_with_retry(method: str, url: str, **kwargs) -> requests.Response:
    """Send an HTTP request, retrying transient failures with exponential backoff.

    Parameters
    ----------
    method
        The HTTP method to use, e.g. `"get"` or `"post"`.
    url
        The URL to send the request to.
    **kwargs
        Additional keyword arguments passed to `requests.request`.

    Returns
    -------
    requests.Response
        The first response that is not a transient failure. If every attempt
        fails transiently, the last response is returned so callers can apply
        their usual error handling.

    Raises
    ------
    requests.ConnectionError
        If the request could not be sent at all and all retries are exhausted.
    requests.Timeout
        If every attempt timed out.

    Notes
    -----
    Responses with status 429, 500, 502, 503 or 504, as well as connection
    errors and timeouts, are retried. The `Retry-After` header of 429
    responses is honored; otherwise the delay grows exponentially with the
    `retry_backoff_factor` configuration value, with jitter added to avoid
    synchronized retries. Set `max_retries` to 0 to disable retries.
    """
    max_retries = config.max_retries
    backoff_factor = config.retry_backoff_factor

    response: requests.Response | None = None
    last_error: Exception | None = None
    for attempt in range(max_retries + 1):
        try:
            response = requests.request(method, url, **kwargs)
        except (requests.Timeout, requests.ConnectionError) as error:
            response = None
            last_error = error
        else:
            last_error = None
            if response.status_code not in _RETRYABLE_STATUS_CODES:
                return response

        if attempt < max_retries:
            time.sleep(_retry_delay(response, attempt, backoff_factor))

    if response is not None:
        return response
    raise last_error  # type: ignore[misc]


def _retry_delay(
    response: requests.Response | None,
    attempt: int,
    backoff_factor: float,
) -> float:
    """Compute the delay, in seconds, before the next retry attempt.

    Honors the `Retry-After` header of 429 responses. Otherwise the delay
    grows exponentially with the attempt number, with jitter applied.
    """
    if response is not None and response.status_code == HTTPStatus.TOO_MANY_REQUESTS:
        retry_after = response.headers.get("Retry-After")
        if retry_after is not None:
            try:
                return max(0.0, float(retry_after))
            except ValueError:
                pass
    return backoff_factor * (2**attempt) * random.uniform(0.5, 1.0)


def format_response(response: list | dict, data_format: Literal["pandas", "json"]) -> pd.Series | pd.DataFrame | dict | list:
    """Format the response data based on the specified format.

    Parameters
    ----------
        response (list | dict): The response data to format.
        data_format (Literal["pandas", "json"]): The desired format for the response.
            For "json" formats, the returned type is a json decoded type, i.e. a dict or a list.

    Returns
    -------
        pd.Series | pd.DataFrame | dict: The formatted response data.

    Raises
    ------
        Exception: If the specified format is invalid or not supported.
    """
    if data_format == "pandas":
        if isinstance(response, dict):
            return pd.Series(response)
        if isinstance(response, list):
            return pd.DataFrame(response)
    elif data_format == "json" and (isinstance(response, dict) or isinstance(response, list)):
        return response

    raise Exception(f"Format: {data_format} invalid or not supported for responses of {type(response)=}.")


def wrap_calls(asset_type: str, calls: list[Callable], module: str) -> tuple[Callable, ...]:
    wrapper_list = []
    for wrapped in calls:
        wrapper: Callable = partial(wrapped, asset_type=asset_type)
        wrapper = update_wrapper(wrapper, wrapped)
        wrapper.__doc__ = wrapped.__doc__.replace("ASSET_TYPE", asset_type) if wrapped.__doc__ is not None else ""
        wrapper.__module__ = module
        wrapper_list.append(wrapper)

    return tuple(wrapper_list)


class EndpointUndefinedError(Exception):
    """Raised when a function tries to connect to an endpoint that does not exist."""

    pass


class ServerError(RuntimeError):
    """Raised for any server error that does not (yet) have better client-side handling."""

    def __init__(self, response: requests.Response):
        self.status_code = response.status_code
        self.detail = response.json().get("detail")
        self.reference = response.json().get("reference")
        self._response = response
