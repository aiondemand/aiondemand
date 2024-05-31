import http.client
import requests
from keycloak import KeycloakOpenID, KeycloakAuthenticationError, ConnectionManager
from typing import Sequence, NamedTuple

from aiod.configuration import config


class KeycloakOpenID_(KeycloakOpenID):
    def __init__(self, server_url, realm_name, client_id):
        super().__init__(server_url, realm_name, client_id)
        self.server_url = server_url

    def reset_connection(self, server_url: str):
        self.server_url = server_url
        self.connection = ConnectionManager(base_url=server_url)


keycloak_openid = KeycloakOpenID_(
    server_url=config.auth_server_url,
    client_id=config.client_id,
    realm_name=config.realm,
)


class User(NamedTuple):
    name: str
    roles: Sequence[str]


def login(username: str, password: str) -> None:
    """Logs in the user with the provided username and password.

    Args:
        username (str): The username of the user.
        password (str): The password of the user.

    Raises:
        FailedAuthenticationError: If the username or password is missing or wrong.
    """
    if username is None or password is None:
        raise FailedAuthenticationError(
            "Username and/or password missing! Please provide your credentials and try again."
        )

    if config.auth_server_url != keycloak_openid.server_url:
        keycloak_openid.reset_connection(server_url=config.auth_server_url)

    try:
        token = keycloak_openid.token(username, password)
    except KeycloakAuthenticationError as e:
        raise FailedAuthenticationError(
            "Authentication failed! Please verify your credentials."
        ) from e
    config.access_token = token["access_token"]
    config.refresh_token = token["refresh_token"]


def logout() -> None:
    """Logs out the current user."""
    keycloak_openid.logout(config.refresh_token)
    config.access_token = None
    config.refresh_token = None


def get_current_user() -> User:
    """Return name and roles of the user that is currently authenticated.

    Raises:
        NotAuthenticatedError: When the user is not authenticated.

    Returns:
        User: The user information for the currently authenticated user.
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
