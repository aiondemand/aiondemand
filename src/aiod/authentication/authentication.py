import http.client
import requests
import time
from keycloak import KeycloakOpenID, KeycloakAuthenticationError, KeycloakPostError
from typing import Sequence, NamedTuple

from aiod.configuration import config


_keycloak_openid: KeycloakOpenID | None = None


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


class User(NamedTuple):
    name: str
    roles: Sequence[str]


def login(username: str, password: str) -> None:
    """
    Logs in the user with the provided username and password (legacy flow).
    """
    if not username:
        raise ValueError("Username must be a non-empty string.")
    if not password:
        raise ValueError("Password must be a non-empty string.")

    try:
        token = keycloak_openid().token(username, password)
    except KeycloakAuthenticationError as e:
        raise FailedAuthenticationError(
            "Authentication failed! Please verify your credentials."
        ) from e
    config.access_token = token["access_token"]
    config.refresh_token = token["refresh_token"]


def login_device_flow(poll_interval: int = 5, timeout: int = 300) -> None:
    """
    Logs in the user using OAuth2 Device Authorization Grant (device flow).
    Shows the user a verification URL + code, then polls until login is complete.
    """
    try:
        device = keycloak_openid().device()

        print(f"To authenticate, please visit {device['verification_uri']} "
              f"and enter the code: {device['user_code']}")

        token_endpoint = keycloak_openid().well_known()["token_endpoint"]

        start_time = time.time()
        while time.time() - start_time < timeout:
            response = requests.post(
                token_endpoint,
                data={
                    "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                    "device_code": device["device_code"],
                    "client_id": config.client_id,
                },
            )
            if response.status_code == 200:
                token = response.json()
                config.access_token = token["access_token"]
                config.refresh_token = token["refresh_token"]
                return
            elif response.status_code == 400 and response.json().get("error") == "authorization_pending":
                time.sleep(poll_interval)
                continue
            else:
                raise FailedAuthenticationError(f"Unexpected error: {response.json()}")

        raise FailedAuthenticationError("Authentication timed out.")

    except KeycloakAuthenticationError as e:
        raise FailedAuthenticationError(
            "Device flow authentication failed!"
        ) from e


def logout(ignore_post_error: bool = False) -> None:
    """
    Logs out the current user by revoking the refresh token (if any).
    """
    try:
        if config.refresh_token:
            keycloak_openid().logout(config.refresh_token)
    except KeycloakPostError as e:
        if not ignore_post_error:
            raise e

    config.access_token = None
    config.refresh_token = None


def get_current_user() -> User:
    """
    Return name and roles of the currently authenticated user.
    """
    if not config.access_token:
        raise NotAuthenticatedError("No active access token")

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
