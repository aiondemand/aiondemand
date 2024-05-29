import http.client
import requests
from typing import Sequence, NamedTuple

from aiod.config.settings import api_base_url


class User(NamedTuple):
    name: str
    roles: Sequence[str]


class NotAuthenticatedError(Exception):
    """Raised when an endpoint that requires authentication is called without authentication."""


def get_current_user() -> User:
    """Return name and roles of the user that is currently authenticated.

    Raises:
        NotAuthenticatedError: When the user is not authenticated.

    Returns:
        User: The user information for the currently authenticated user.
    """
    response = requests.get(f"{api_base_url}authorization_test")
    content = response.json()
    if response.status_code == http.client.UNAUTHORIZED:
        raise NotAuthenticatedError(content)
    return User(
        name=content["name"],
        roles=tuple(content["roles"]),
    )
