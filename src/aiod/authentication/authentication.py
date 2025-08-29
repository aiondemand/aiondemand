import datetime
import time
import http.client
from http import HTTPStatus
from pathlib import Path

import requests
import tomlkit
from typing import Sequence, NamedTuple
from keycloak import KeycloakOpenID, KeycloakPostError

from aiod.configuration import config
import logging

logger = logging.getLogger(__name__)


def _datetime_utc_in(*, seconds: int) -> datetime.datetime:
    span = datetime.timedelta(seconds=seconds)
    return datetime.datetime.now(datetime.UTC) + span


class Token:
    def __init__(
        self,
        refresh_token: str,
        access_token: str | None = None,
        expires_in_seconds: int = -1,
    ):
        if expires_in_seconds > 0 and access_token is None:
            raise ValueError(
                "If `expires_in_seconds` is set, `access_token` must be set to a valid access_token"
            )
        self._refresh_token = refresh_token
        self._access_token = access_token or ""
        self._expiration_date = _datetime_utc_in(seconds=expires_in_seconds)

    @property
    def has_expired(self) -> bool:
        return datetime.datetime.now(datetime.UTC) >= self._expiration_date

    @property
    def bearer_token(self) -> str:
        if not self.has_expired:
            return self._access_token
        self.refresh()
        return self._access_token

    def refresh(self):
        token_info = keycloak_openid().refresh_token(self._refresh_token)
        self._access_token = token_info["access_token"]
        # self._refresh_token = token_info["refresh_token"]  # Only with auto-rotating
        # Because of the minuscule time difference between the server sending the
        # response and us processing it, the `expires_in` may not be used directly
        # when calculating expiration time.
        SAFETY_PERIOD_SECONDS = 2
        self._expiration_date = _datetime_utc_in(
            token_info["expires_in"] - SAFETY_PERIOD_SECONDS
        )
        logger.info(f"Renewed access token, it expires {self._expiration_date}.")
        return self.access_token

    def __str__(self):
        return self._refresh_token

    def to_file(self, file: Path | None = None):
        file = file or _user_token_file
        doc = tomlkit.document()
        doc.add("refresh_token", self._refresh_token)
        if not self.has_expired:
            doc.add("access_token", self._access_token)
            doc.add("expiration_date", self._expiration_date.isoformat())
        file.write_text(tomlkit.dumps(doc))

    @classmethod
    def from_file(cls, file: Path | None = None) -> "Token":
        file = file or _user_token_file
        doc = tomlkit.parse(file.read_text())
        kwargs = {"refresh_token": doc["refresh_token"]}
        if "expiration_date" in doc:
            expiration_date = datetime.datetime.fromisoformat(doc["expiration_date"])
            expires_in = expiration_date - _datetime_utc_in(seconds=0)
            if expires_in.total_seconds() > 0:
                kwargs.update(
                    {
                        "access_token": doc["access_token"],
                        "expires_in_seconds": expires_in.seconds,
                    }
                )
        return Token(**kwargs)


def _connect_keycloak() -> KeycloakOpenID:
    return KeycloakOpenID(
        server_url=config.auth_server,
        client_id=config.client_id,
        realm_name=config.realm,
    )


def keycloak_openid() -> KeycloakOpenID:
    global _keycloak_openid
    if _keycloak_openid is None:
        _keycloak_openid = _connect_keycloak()
    return _keycloak_openid


def _on_keycloak_config_changed(_: str, __: str, ___: str) -> None:
    global _keycloak_openid
    invalidate_api_key(ignore_post_error=True)
    _keycloak_openid = None


config.subscribe("auth_server", on_change=_on_keycloak_config_changed)
config.subscribe("realm", on_change=_on_keycloak_config_changed)
config.subscribe("client_id", on_change=_on_keycloak_config_changed)

_keycloak_openid: KeycloakOpenID | None = None


class User(NamedTuple):
    name: str
    roles: Sequence[str]


def renew_token(api_key: str | None = None) -> str:
    """Tries to renew the current API key."""
    if not api_key and not config.token:
        raise ValueError(
            "Either `api_key` or `config.refresh_token` must be a non-empy string."
        )
    refresh_token = api_key or config.token
    token_info = keycloak_openid().refresh_token(refresh_token)
    config._access_token = token_info["access_token"]
    config.token = token_info["refresh_token"]
    expiration_span = datetime.timedelta(seconds=token_info["expires_in"])
    logger.info(f"New token expires in {expiration_span}.")
    return config.token


def get_token(
    max_wait_time_seconds: int = 300,
    *,
    write_to_file: bool = False,
) -> Token:
    """Get an API Key by prompting the user to log in through a browser.

    Args:
        max_wait_time_seconds: int (default = 300)
            The maximum time this function blocks waiting for the authentication workflow
            to complete. If `max_wait_time_seconds` seconds have elapsed without successful
            authentication, this function raises an AuthenticationError.
            This must be set to a positive integer.
        write_to_file: bool (default = False)
            If set to true, the new api key (refresh token) will automatically be saved to
            the user configuration file (~/.aiod/config.toml).

    Returns:
        Token: The new token for use in authenticated requests.

    Raises:
        AuthenticationError: if authentication is unsuccessful in any way.

    """
    if max_wait_time_seconds <= 0 or not isinstance(max_wait_time_seconds, int):
        raise ValueError("`max_wait_time` must be a positive integer.")
    kc = keycloak_openid()

    response = kc.device()
    device_code = response["device_code"]
    user_code = response["user_code"]
    verification_uri = response["verification_uri"]
    verification_uri_complete = response["verification_uri_complete"]

    # We print instead of log because this information *needs* to get to the user,
    # and relying on user logging configurations is too finnicky for that.
    print("Please authenticate using one of two methods:")  # noqa: T201
    print()  # noqa: T201
    print(f"  1. Navigate to {verification_uri_complete}")  # noqa: T201
    print(  # noqa: T201
        f"  2. Navigate to {verification_uri} and enter code {user_code}"
    )
    print()  # noqa: T201
    print(  # noqa: T201
        f"This workflow will automatically abort after {max_wait_time_seconds} seconds."
    )

    poll_interval = response["interval"]
    start_time = time.time()

    token_endpoint = kc.well_known()["token_endpoint"]
    token_data = {
        "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
        "client_id": config.client_id,
        "device_code": device_code,
    }
    # We do not know when the user finishes their authentication, so we poll the server
    while time.time() - start_time < max_wait_time_seconds:
        time.sleep(poll_interval)
        token_response = requests.post(token_endpoint, data=token_data)
        token_response_data = token_response.json()

        response = (token_response.status_code, token_response_data.get("error"))
        match response:
            case (HTTPStatus.OK, _):
                access_token = token_response_data["access_token"]
                kc.decode_token(access_token, validate=True)
                token = Token(
                    refresh_token=token_response_data["refresh_token"],
                    access_token=access_token,
                    expires_in_seconds=token_response_data["expires_in"],
                )
                config._access_token = token._access_token
                config._refresh_token = token._refresh_token
                if write_to_file:
                    token.to_file(_user_token_file)
                return token
            case (HTTPStatus.BAD_REQUEST, "authorization_pending"):
                continue
            case (HTTPStatus.BAD_REQUEST, "slow_down"):
                poll_interval *= 1.5
                continue
            case (HTTPStatus.BAD_REQUEST, "access_denied"):
                raise AuthenticationError("Access denied by Keycloak server.")
            case (HTTPStatus.BAD_REQUEST, "expired_token"):
                raise AuthenticationError("Device code has expired, please try again.")
            case (status, error):
                raise AuthenticationError(
                    f"Unexpected error, please contact the developers ({status}, {error})."
                )
    raise AuthenticationError(
        f"No successful authentication within {max_wait_time_seconds=} seconds."
    )


def invalidate_api_key(
    api_key: str | None = None, ignore_post_error: bool = False
) -> None:
    """Invalidates the current (or provided) API key.

    Ends the current keycloak session, invalidating all keys issued.
    Args:
        ignore_post_error:
            If true, do not raise an error if the logout attempt failed.
    """
    token = api_key or config.token
    try:
        keycloak_openid().logout(token)
    except KeycloakPostError as e:
        if not ignore_post_error:
            raise e
    config._access_token = ""
    config.token = ""


def get_current_user() -> User:
    """Return name and roles of the user that is currently authenticated.

    Returns:
        User: The user information for the currently authenticated user.

    Raises:
        NotAuthenticatedError: When the user is not authenticated.
    """
    response = requests.get(
        f"{config.api_server}authorization_test",
        headers={"Authorization": f"Bearer {config._access_token}"},
    )

    content = response.json()
    if response.status_code == http.client.UNAUTHORIZED:
        raise NotAuthenticatedError(content)
    return User(
        name=content["name"],
        roles=tuple(content["roles"]),
    )


class AuthenticationError(Exception):
    """Raised when an authentication error occurred."""


class NotAuthenticatedError(Exception):
    """Raised when an endpoint that requires authentication is called without authentication."""


_user_token_file = Path("~/.aiod/token.toml").expanduser()
