"""Custom exceptions for the AIoD Python SDK."""

import requests


class AIoDException(Exception):
    """Base exception for all AIoD related errors."""
    pass


class EndpointUndefinedError(AIoDException):
    """Raised when a function tries to connect to an endpoint that does not exist."""
    pass


class APIError(AIoDException):
    """Base exception for all HTTP-related API errors.

    Attributes
    ----------
    response : requests.Response
        The HTTP response associated with this error.
    status_code : int
        The HTTP status code.
    detail : str | None
        The detail message provided by the server.
    reference : str | None
        The reference ID provided by the server.
    """

    def __init__(self, response: requests.Response, detail: str | None = None, reference: str | None = None):
        self.response = response
        self.status_code = response.status_code
        try:
            json_response = response.json()
            self.detail = detail or json_response.get("detail")
            self.reference = reference or json_response.get("reference")
        except ValueError:
            # Handle non-JSON responses gracefully (fixes issue #88 implicitly)
            self.detail = detail or response.text
            self.reference = reference

        if self.detail:
            message = f"API Error {self.status_code}: {self.detail}"
        else:
            message = f"API Error {self.status_code} on {response.request.method} {response.url}"
        
        super().__init__(message)


class AssetNotFoundError(APIError):
    """Raised when an asset (e.g., dataset, model) could not be found via the API.
    
    This replaces typical KeyError raise patterns when resources are missing.
    """
    pass


class RateLimitError(APIError):
    """Raised when the API rate limit has been exceeded (HTTP 429)."""
    pass


class AuthenticationError(APIError):
    """Raised for authentication or authorization failures (HTTP 401 or 403)."""
    pass


class ServerError(APIError):
    """Raised for general server errors (HTTP 5xx) that aren't specifically handled."""
    pass
