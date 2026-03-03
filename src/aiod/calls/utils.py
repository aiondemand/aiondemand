import logging
import random
import time
from collections.abc import Callable
from functools import partial, update_wrapper
from http import HTTPStatus
from typing import Literal

import pandas as pd
import requests

logger = logging.getLogger(__name__)

# HTTP status codes considered transient — safe to retry
_RETRYABLE_STATUSES = {
    HTTPStatus.TOO_MANY_REQUESTS,      # 429
    HTTPStatus.INTERNAL_SERVER_ERROR,  # 500
    HTTPStatus.BAD_GATEWAY,            # 502
    HTTPStatus.SERVICE_UNAVAILABLE,    # 503
    HTTPStatus.GATEWAY_TIMEOUT,        # 504
}

# These HTTP methods are non-idempotent — never retry to avoid duplicate side-effects
_NON_RETRYABLE_METHODS = {"POST", "PATCH"}


def _request_with_retry(method: str, url: str, **kwargs) -> requests.Response:
    """Make an HTTP request with automatic retry for transient errors.

    Retries are performed for responses with status codes in ``_RETRYABLE_STATUSES``
    and for ``requests.Timeout`` / ``requests.ConnectionError`` exceptions.

    ``POST`` and ``PATCH`` are **never** retried because they are non-idempotent
    and a silent duplicate could cause unintended side-effects (e.g., registering
    the same asset twice).

    The wait time between attempts follows exponential backoff with jitter::

        wait = backoff_factor * 2**attempt + random(0, 1)

    For ``429 Too Many Requests`` responses, the ``Retry-After`` header is
    respected when present.

    Parameters
    ----------
    method:
        HTTP method string, e.g. ``'GET'``, ``'DELETE'``, ``'PUT'``.
    url:
        The URL to request.
    **kwargs:
        Additional keyword arguments forwarded to ``requests.request()``.

    Returns
    -------
    :
        The ``requests.Response`` for the first non-retryable response.

    Raises
    ------
    RuntimeError
        If ``method`` is ``POST`` or ``PATCH`` (programming guard — callers
        should use ``requests.post`` / ``requests.patch`` directly).
    requests.Timeout
        If the request times out on every retry attempt.
    requests.ConnectionError
        If a connection error occurs on every retry attempt.
    """
    from aiod.configuration import config  # local import avoids circular dependency

    upper_method = method.upper()
    if upper_method in _NON_RETRYABLE_METHODS:
        raise RuntimeError(
            f"_request_with_retry does not support {upper_method} — "
            "use requests.post/patch directly to avoid unintended duplicates."
        )

    max_retries = config.max_retries
    backoff = config.retry_backoff_factor
    last_res: requests.Response | None = None

    for attempt in range(max_retries + 1):
        try:
            res = requests.request(upper_method, url, **kwargs)
        except (requests.Timeout, requests.ConnectionError) as exc:
            if attempt == max_retries:
                raise
            wait = backoff * (2 ** attempt) + random.random()
            logger.warning(
                "Request to %r failed with %s (attempt %d/%d). Retrying in %.1fs.",
                url, type(exc).__name__, attempt + 1, max_retries + 1, wait,
            )
            time.sleep(wait)
            continue

        if res.status_code not in _RETRYABLE_STATUSES or attempt == max_retries:
            return res

        # Respect Retry-After header for 429; fall back to exponential backoff.
        if res.status_code == HTTPStatus.TOO_MANY_REQUESTS:
            retry_after = res.headers.get("Retry-After")
            wait = float(retry_after) if retry_after else backoff * (2 ** attempt) + random.random()
        else:
            wait = backoff * (2 ** attempt) + random.random()

        logger.warning(
            "Request to %r returned HTTP %d (attempt %d/%d). Retrying in %.1fs.",
            url, res.status_code, attempt + 1, max_retries + 1, wait,
        )
        last_res = res
        time.sleep(wait)

    # All retries exhausted — return the last failing response so callers
    # can raise the appropriate typed error (ServerError, KeyError, etc.).
    return last_res  # type: ignore[return-value]


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
