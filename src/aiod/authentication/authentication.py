import time
import http.client
import requests
import jwt
from jwt import PyJWKClient
from typing import Sequence, NamedTuple
from keycloak import KeycloakOpenID, KeycloakAuthenticationError, KeycloakPostError

from aiod.configuration import config
import logging

logger = logging.getLogger(__name__)


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


def login_device_flow(poll_interval: int = 0) -> None:
    """Logs in the user via device flow (for long-term tokens)."""
    kc = keycloak_openid()
    response = kc.device()
    device_code = response["device_code"]
    user_code = response["user_code"]
    verification_uri = response["verification_uri"]
    verification_uri_complete = response["verification_uri_complete"]
    interval = poll_interval or response["interval"]

    logger.info(
        "Device code: %s, verification URL: %s",
        "verification URL complete: %s",
        user_code,
        verification_uri,
        verification_uri_complete,
    )

    # Poll token endpoint until approved
    token_endpoint = kc.well_known()["token_endpoint"]
    jwks_endpoint = kc.well_known()["jwks_uri"]

    while True:
        time.sleep(interval)
        token_data = {
            "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
            "client_id": config.client_id,
            "device_code": device_code,
        }
        token_response = requests.post(token_endpoint, data=token_data)
        token_response_data = token_response.json()

        if token_response.status_code == 200:
            config.access_token = token_response_data["access_token"]
            config.refresh_token = token_response_data.get("refresh_token")

            _validate_token(config.access_token, jwks_endpoint)  # type: ignore[arg-type]
            # print("Device flow login successful.")
            break
        elif token_response.status_code == 400:
            error = token_response_data.get("error")
            if error == "authorization_pending":
                continue
            elif error == "slow_down":
                interval += 5
            else:
                raise FailedAuthenticationError(f"Device flow error: {error}")
        else:
            raise FailedAuthenticationError("Unexpected device flow error.")


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


def _validate_token(access_token: str, jwks_endpoint: str) -> dict:
    """Validate JWT signature and audience using JWKS."""
    if access_token is None:
        raise FailedAuthenticationError("No access token to validate")
    decoded_token = jwt.decode(access_token, options={"verify_signature": False})
    aud = decoded_token["aud"]

    jwks_client = PyJWKClient(jwks_endpoint)
    signing_key = jwks_client.get_signing_key_from_jwt(access_token).key
    return jwt.decode(access_token, signing_key, algorithms=["RS256"], audience=aud)


class FailedAuthenticationError(Exception):
    """Raised when an authentication error occurred."""


class NotAuthenticatedError(Exception):
    """Raised when an endpoint that requires authentication is called without authentication."""
