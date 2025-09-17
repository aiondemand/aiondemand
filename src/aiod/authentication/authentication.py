import datetime
import time
import http.client
from http import HTTPStatus
import functools
from pathlib import Path

import requests
import tomlkit
from typing import Sequence, NamedTuple
from keycloak import KeycloakOpenID, KeycloakPostError, KeycloakConnectionError

from aiod.configuration import config
import logging

logger = logging.getLogger(__name__)

_token: "Token | None" = None
_user_token_file = Path("~/.aiod/token.toml").expanduser()


@functools.cache
def keycloak_openid() -> KeycloakOpenID:
    secret = (_token._client_secret or None) if _token else None
    return KeycloakOpenID(
        server_url=config.auth_server,
        client_id=config.client_id,
        realm_name=config.realm,
        client_secret_key=secret,
    )


def _on_keycloak_config_changed(_: str, __: str, ___: str) -> None:
    keycloak_openid.cache_clear()


config.subscribe("auth_server", on_change=_on_keycloak_config_changed)
config.subscribe("realm", on_change=_on_keycloak_config_changed)
config.subscribe("client_id", on_change=_on_keycloak_config_changed)


def _datetime_utc_in(*, seconds: int) -> datetime.datetime:
    span = datetime.timedelta(seconds=seconds)
    return datetime.datetime.now(datetime.UTC) + span


class Token:
    """Ensures active access tokens provided through one dedicated refresh token."""

    def __init__(
        self,
        *,
        client_secret: str | None = None,
        refresh_token: str | None = None,
        access_token: str | None = None,
        expires_in_seconds: int = -1,
    ):
        if (client_secret and refresh_token) or not (client_secret or refresh_token):
            raise ValueError(
                "Must set exactly one of `client_secret` or `refresh_token`."
            )
        if expires_in_seconds > 0 and access_token is None:
            raise ValueError(
                "If `expires_in_seconds` is set, `access_token` must be set to a valid access_token"
            )
        self._client_secret = client_secret
        self._refresh_token = refresh_token
        self._access_token = access_token or ""
        self._expiration_date = _datetime_utc_in(seconds=expires_in_seconds)

    @property
    def has_expired(self) -> bool:
        """Return whether the *access token* has expired based on local data."""
        return datetime.datetime.now(datetime.UTC) >= self._expiration_date

    @property
    def headers(self) -> dict[str, str]:
        """HTTP authorization header data for the token.

        Examples
        --------
        ```python
        import aiod
        token = aiod.get_token()
        requests.post(url, headers=token.headers, json=metadata)
        ```

        """
        if self.has_expired:
            self._refresh()
        return {"Authorization": f"Bearer {self._access_token}"}

    def __str__(self):
        return self._refresh_token

    def _refresh(self) -> None:
        """Use the `refresh token` or `client_secret` to request a new `access token`."""
        try:
            if self._refresh_token:
                token_info = keycloak_openid().refresh_token(self._refresh_token)
            if self._client_secret:
                token_info = keycloak_openid().token(grant_type="client_credentials")
        except KeycloakPostError:
            raise AuthenticationError(
                "Refresh token is not valid. Use `aiod.create_token` to get a new one."
            ) from None
        except KeycloakConnectionError as e:
            e.add_note(f"Could not connect {config.auth_server!r}, try again later.")
            raise

        self._access_token = token_info["access_token"]
        # self._refresh_token = token_info["refresh_token"]  # Only with auto-rotating
        # Because of the minuscule time difference between the server sending the
        # response and us processing it, the `expires_in` may not be used directly
        # when calculating expiration time.
        SAFETY_PERIOD_SECONDS = 2
        self._expiration_date = _datetime_utc_in(
            seconds=token_info["expires_in"] - SAFETY_PERIOD_SECONDS
        )
        logger.info(f"Renewed access token, it expires {self._expiration_date}.")

    def to_file(self, file: Path | None = None):
        doc = tomlkit.document()
        if self._refresh_token:
            doc.add("refresh_token", self._refresh_token)
        if self._client_secret:
            doc.add("client_secret", self._client_secret)
        if not self.has_expired:
            doc.add("access_token", self._access_token)
            doc.add("expiration_date", self._expiration_date.isoformat())

        file = file or _user_token_file
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(tomlkit.dumps(doc))

    @classmethod
    def from_file(cls, file: Path | None = None) -> "Token":
        file = file or _user_token_file
        doc = tomlkit.parse(file.read_text())
        kwargs: dict[str, str | int] = {
            "refresh_token": str(doc.get("refresh_token", "")),
            "client_secret": str(doc.get("client_secret", "")),
        }
        if "expiration_date" in doc:
            expiration_date = datetime.datetime.fromisoformat(doc["expiration_date"])
            expires_in = expiration_date - _datetime_utc_in(seconds=0)
            if expires_in.total_seconds() > 0:
                kwargs.update(
                    {
                        "access_token": str(doc["access_token"]),
                        "expires_in_seconds": expires_in.seconds,
                    }
                )
        return Token(**kwargs)  # type: ignore[arg-type]


def set_token(token: Token) -> None:
    """Set the token directly.

    Parameters
    ----------
    token
        Sets the token to be used for authenticated requests.

    Notes
    -----
    This function does not validate the provided token.
    If the token is invalid, subsequent authenticated requests may fail.
    """
    global _token
    _token = token
    keycloak_openid.cache_clear()


def get_token() -> Token:
    """Get the currently configured token that is used for authenticated requests.

    Returns
    -------
    :
    """
    if _token is None:
        msg = (
            "No token set. Please create a new token with `aiod.create_token()`,"
            " or set one with `aiod.set_token('...')`."
        )
        raise NotAuthenticatedError(msg)
    return _token


def _get_auth_headers(*, required: bool = True) -> dict:
    try:
        return get_token().headers
    except (AuthenticationError, NotAuthenticatedError):
        if required:
            raise
    return {}


def create_token(
    timeout_seconds: int = 300,
    *,
    write_to_file: bool = False,
    use_in_requests: bool = True,
) -> Token:
    """Get an API Key by prompting the user to log in through a browser.

    Notes
    -----
    This is a blocking function, and will poll the authentication server until
    authentication is completed or `timeout_seconds` have passed.

    Parameters
    ----------
    timeout_seconds
        The maximum time this function blocks waiting for the authentication workflow
        to complete. If `timeout_seconds` seconds have elapsed without successful
        authentication, this function raises an AuthenticationError.
        This must be set to a positive integer.
    write_to_file
        If set to true, the new api key (refresh token) will automatically be saved to
        the user configuration file (~/.aiod/config.toml).
    use_in_requests
        If set to true, the new token will automatically be used for future authenticated
        requests.

    Returns
    -------
    :
        The new token for use in authenticated requests.

    Raises
    ------
    AuthenticationError
        If authentication is unsuccessful in any way.

    """
    if timeout_seconds <= 0 or not isinstance(timeout_seconds, int):
        raise ValueError("`timeout_seconds` must be a positive integer.")
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
        f"This workflow will automatically abort after {timeout_seconds} seconds."
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
    while time.time() - start_time < timeout_seconds:
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
                if write_to_file:
                    token.to_file(_user_token_file)
                if use_in_requests:
                    set_token(token)
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
        f"No successful authentication within {timeout_seconds=} seconds."
    )


def invalidate_token(
    token: str | Token | None = None, ignore_errors: bool = False
) -> None:
    """Invalidates the current (or provided) API key.

    Ends the current keycloak session, invalidating all keys issued.

    Parameters
    ----------
    token
        The token to invalidate.
        If str, it should be a refresh token.
        If None, it will default to the currently configured token.
    ignore_errors
        If true, do not raise an error if the logout attempt failed.
    """
    global _token
    token = token or _token
    try:
        keycloak_openid().logout(token)
    except (KeycloakPostError, KeycloakConnectionError) as e:
        if not ignore_errors:
            raise e
    finally:
        _token = None


class User(NamedTuple):
    name: str
    roles: Sequence[str]


def get_current_user() -> User:
    """Return name and roles of the user that is currently authenticated.

    Returns
    -------
    User
        The user information for the currently authenticated user.

    Raises
    ------
    NotAuthenticatedError
        When the user is not authenticated.
    """
    response = requests.get(
        f"{config.api_server}authorization_test",
        headers=get_token().headers,
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


if _user_token_file.exists() and _user_token_file.is_file():
    try:
        _token = Token.from_file(_user_token_file)
    except Exception as e:
        e.add_note(f"Failed to load credentials from {str(_user_token_file)!r}")
        raise e
