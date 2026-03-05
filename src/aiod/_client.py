"""Centralized HTTP client for the AIoD SDK."""

import asyncio
import logging
import time
from dataclasses import dataclass
from functools import cached_property

import httpx

from aiod.authentication.authentication import _get_auth_headers
from aiod.configuration._config import config

logger = logging.getLogger(__name__)


class AiodHTTPError(RuntimeError):
    """Base class for HTTP errors returned by the AIoD API."""

    def __init__(self, response: httpx.Response):
        self.status_code = response.status_code
        try:
            body = response.json()
        except Exception:
            body = {}
        self.detail = body.get("detail")
        self.reference = body.get("reference")
        super().__init__(f"HTTP {self.status_code}: {self.detail}")


class AiodNotFoundError(AiodHTTPError):
    """Raised when the server returns 404 Not Found."""


class AiodForbiddenError(AiodHTTPError):
    """Raised when the server returns 403 Forbidden."""


class AiodRateLimitError(AiodHTTPError):
    """Raised when the server returns 429 Too Many Requests.

    Attributes
    ----------
    retry_after : float | None
        Seconds to wait before retrying, parsed from the ``Retry-After``
        response header.  ``None`` if the header is absent or unparseable.
    """

    def __init__(self, response: httpx.Response):
        super().__init__(response)
        value = response.headers.get("retry-after")
        try:
            self.retry_after: float | None = float(value) if value is not None else None
        except ValueError:
            self.retry_after = None


class AiodServerError(AiodHTTPError):
    """Raised when the server returns a 5xx error."""


def _raise_for_status(response: httpx.Response) -> None:
    """Raise an appropriate exception for non-2xx responses."""
    if response.is_success:
        return
    status = response.status_code
    if status == 401:
        # Lazy import to avoid circular dependency
        from aiod.authentication.authentication import NotAuthenticatedError

        try:
            detail = response.json().get("detail", "Unauthorized")
        except Exception:
            detail = "Unauthorized"
        raise NotAuthenticatedError(detail)
    if status == 403:
        raise AiodForbiddenError(response)
    if status == 404:
        raise AiodNotFoundError(response)
    if status == 429:
        raise AiodRateLimitError(response)
    if status >= 500:
        raise AiodServerError(response)
    raise AiodHTTPError(response)


class BearerAuth(httpx.Auth):
    """Injects a fresh bearer token into every request."""

    def __init__(self, required: bool = False):
        self._required = required

    def auth_flow(self, request: httpx.Request):
        request.headers.update(_get_auth_headers(required=self._required))
        yield request


class RetryTransport(httpx.AsyncBaseTransport, httpx.BaseTransport):
    """Wraps an httpx transport and retries on configured status codes.

    Reads retry configuration live from ``config`` on every request so that
    changes to ``config.max_retries`` etc. take effect immediately.
    """

    METHODS = frozenset(["GET", "PUT", "DELETE", "HEAD", "OPTIONS"])

    def __init__(
        self,
        wrapped: httpx.BaseTransport | None = None,
        async_wrapped: httpx.AsyncBaseTransport | None = None,
    ):
        self._sync_transport = wrapped or httpx.HTTPTransport()
        self._async_transport = async_wrapped or httpx.AsyncHTTPTransport()

    def _backoff(self, attempt: int) -> float:
        delay = config.retry_backoff_factor * (2 ** (attempt - 1))
        return min(delay, config.max_backoff)

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        if request.method not in self.METHODS:
            return self._sync_transport.handle_request(request)

        for attempt in range(config.max_retries + 1):
            try:
                response = self._sync_transport.handle_request(request)
                if (
                    response.status_code not in config.retry_status_codes
                    or attempt == config.max_retries
                ):
                    return response
                if config.debug_http:
                    logger.debug(
                        "retry %d/%d (status=%d)",
                        attempt + 1,
                        config.max_retries,
                        response.status_code,
                    )
            except httpx.TransportError as exc:
                if attempt == config.max_retries:
                    raise
                if config.debug_http:
                    logger.debug(
                        "retry %d/%d (TransportError: %s)",
                        attempt + 1,
                        config.max_retries,
                        exc,
                    )
            time.sleep(self._backoff(attempt + 1))
        return response  # type: ignore[return-value]

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        if request.method not in self.METHODS:
            return await self._async_transport.handle_async_request(request)

        for attempt in range(config.max_retries + 1):
            try:
                response = await self._async_transport.handle_async_request(request)
                if (
                    response.status_code not in config.retry_status_codes
                    or attempt == config.max_retries
                ):
                    return response
                if config.debug_http:
                    logger.debug(
                        "retry %d/%d (status=%d)",
                        attempt + 1,
                        config.max_retries,
                        response.status_code,
                    )
            except httpx.TransportError as exc:
                if attempt == config.max_retries:
                    raise
                if config.debug_http:
                    logger.debug(
                        "retry %d/%d (TransportError: %s)",
                        attempt + 1,
                        config.max_retries,
                        exc,
                    )
            await asyncio.sleep(self._backoff(attempt + 1))
        return response  # type: ignore[return-value]


@dataclass(frozen=True)
class AiodClient:
    """Thin wrapper around httpx providing sync and async API access.

    Notes
    -----
    All ``path`` arguments must be **absolute URLs**.
    Use :func:`aiod.calls.urls.server_url` or the ``url_to_*`` helpers to
    build them.  Example::

        from aiod.calls.urls import server_url
        client.get(server_url() + "datasets")

    Authentication is injected per-request by :class:`BearerAuth`; read
    methods use an optional token while write methods (``post``, ``put``,
    ``delete``) require a valid token.
    Timeout and retry settings are read live from :data:`aiod.configuration.config`
    so that changes take effect without rebuilding the client.
    """

    @cached_property
    def _sync(self) -> httpx.Client:
        return httpx.Client(
            auth=BearerAuth(required=False),
            transport=RetryTransport(),
        )

    @cached_property
    def _async(self) -> httpx.AsyncClient:
        return httpx.AsyncClient(
            auth=BearerAuth(required=False),
            transport=RetryTransport(),
        )

    def request(self, method: str, path: str, **kwargs) -> httpx.Response:
        kwargs.setdefault("timeout", config.request_timeout_seconds)
        t0 = time.monotonic()
        response = self._sync.request(method, path, **kwargs)
        if config.debug_http:
            elapsed_ms = (time.monotonic() - t0) * 1000
            logger.debug(
                "%s %s → %d (%.0fms)", method, path, response.status_code, elapsed_ms
            )
        _raise_for_status(response)
        return response

    async def arequest(self, method: str, path: str, **kwargs) -> httpx.Response:
        kwargs.setdefault("timeout", config.request_timeout_seconds)
        t0 = time.monotonic()
        response = await self._async.request(method, path, **kwargs)
        if config.debug_http:
            elapsed_ms = (time.monotonic() - t0) * 1000
            logger.debug(
                "%s %s → %d (%.0fms)", method, path, response.status_code, elapsed_ms
            )
        _raise_for_status(response)
        return response

    def get(self, path: str, **kwargs) -> httpx.Response:
        return self.request("GET", path, **kwargs)

    async def aget(self, path: str, **kwargs) -> httpx.Response:
        return await self.arequest("GET", path, **kwargs)

    def post(self, path: str, **kwargs) -> httpx.Response:
        return self.request("POST", path, auth=BearerAuth(required=True), **kwargs)

    def put(self, path: str, **kwargs) -> httpx.Response:
        return self.request("PUT", path, auth=BearerAuth(required=True), **kwargs)

    def delete(self, path: str, **kwargs) -> httpx.Response:
        return self.request("DELETE", path, auth=BearerAuth(required=True), **kwargs)


client = AiodClient()
