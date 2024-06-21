import http.client
import requests
from keycloak import KeycloakOpenID, KeycloakAuthenticationError, KeycloakPostError
from typing import Sequence, NamedTuple

from aiod.configuration import config


def _connect_keycloak() -> KeycloakOpenID:
    return KeycloakOpenID(
        server_url=config.auth_server_url,
        client_id=config.client_id,
        realm_name=config.realm,
    )


def keycloak_openid() -> KeycloakOpenID:
    global _keycloak_openid
    if _keycloak_openid is None:
        _keycloak_openid = _connect_keycloak()
    return _keycloak_openid


def on_keycloak_config_changed(_: str, __: str, ___: str) -> None:
    global _keycloak_openid
    logout(ignore_post_error=True)
    _keycloak_openid = None


config.subscribe("auth_server_url", on_change=on_keycloak_config_changed)
config.subscribe("realm", on_change=on_keycloak_config_changed)
config.subscribe("client_id", on_change=on_keycloak_config_changed)

_keycloak_openid: KeycloakOpenID | None = None


class User(NamedTuple):
    name: str
    roles: Sequence[str]


def login(username: str, password: str) -> None:
    """Logs in the user with the provided username and password.

    Args:
        username (str): The username of the user.
        password (str): The password of the user.

    Raises:
        ValueError: When username or password is empty.
        FailedAuthenticationError: When the username or password is wrong.
    """
    if not username:
        raise ValueError(
            f"{username!r} is not a valid username, must be a non-empty string."
        )
    if not password:
        raise ValueError(
            f"{password!r} is not a valid password, must be a non-empty string."
        )

    try:
        token = keycloak_openid().token(username, password)
    except KeycloakAuthenticationError as e:
        raise FailedAuthenticationError(
            "Authentication failed! Please verify your credentials."
        ) from e
    config.access_token = token["access_token"]
    config.refresh_token = token["refresh_token"]


def logout(ignore_post_error: bool = False) -> None:
    """Logs out the current user.

    Args:
        ignore_post_error:
            If true, do not raise an error if the logout attempt failed.

    """
    try:
        keycloak_openid().logout(config.refresh_token)
    except KeycloakPostError as e:
        if not ignore_post_error:
            raise e

    config.access_token = None
    config.refresh_token = None


def get_current_user() -> User:
    """Return name and roles of the user that is currently authenticated.

    Returns:
        User: The user information for the currently authenticated user.

    Raises:
        NotAuthenticatedError: When the user is not authenticated.
    """
    response = requests.get(
        f"{config.api_base_url}authorization_test",
        headers={"Authorization": f"Bearer {config.access_token}"},
    )

    content = response.json()
    if response.status_code == http.client.UNAUTHORIZED:
        raise NotAuthenticatedError(content)
    return User(
        name=content["name"],
        roles=tuple(content["roles"]),
    )


class FailedAuthenticationError(Exception):
    """Raised when an authentication error occurred."""


class NotAuthenticatedError(Exception):
    """Raised when an endpoint that requires authentication is called without authentication."""
