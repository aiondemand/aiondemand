import os
import time
import jwt
import requests
from jwt import PyJWKClient
from keycloak import KeycloakOpenID
from keycloak.exceptions import KeycloakAuthenticationError, KeycloakGetError

from aiod.configuration import config


class FailedAuthenticationError(Exception):
    """Raised when authentication fails."""


class NotAuthenticatedError(Exception):
    """Raised when accessing an endpoint without valid authentication."""


def _init_keycloak() -> KeycloakOpenID:
    return KeycloakOpenID(
        server_url=f"{config.auth_server_url}/",
        client_id=config.client_id,
        realm_name=config.realm,
    )


def login_device_flow(poll_interval: int | None = None) -> None:
    """Authenticate the user via device authorization flow."""

    keycloak_openid = _init_keycloak()
    well_known = keycloak_openid.well_known()

    token_endpoint = well_known["token_endpoint"]
    jwks_endpoint = well_known["jwks_uri"]

    # Step 1: Request device/user codes
    response = keycloak_openid.device()
    device_code = response["device_code"]
    user_code = response["user_code"]
    verification_uri = response["verification_uri"]
    verification_uri_complete = response["verification_uri_complete"]
    interval = response["interval"]

    if poll_interval:
        interval = poll_interval

    print(f"Please go to {verification_uri} and enter the code: {user_code}")
    print(f"Or visit directly: {verification_uri_complete}")

    # Step 2: Poll until user authorizes
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
            access_token = token_response_data["access_token"]
            refresh_token = token_response_data.get("refresh_token")

            # Verify signature
            decoded = jwt.decode(access_token, options={"verify_signature": False})
            aud = decoded["aud"]
            jwks_client = PyJWKClient(jwks_endpoint)
            signing_key = jwks_client.get_signing_key_from_jwt(access_token).key
            jwt.decode(access_token, signing_key, algorithms=["RS256"], audience=aud)

            # Store tokens in config
            config.access_token = access_token
            config.refresh_token = refresh_token
            return

        elif token_response.status_code == 400:
            error = token_response_data.get("error")
            if error == "authorization_pending":
                continue
            elif error == "slow_down":
                interval += 5
            else:
                raise FailedAuthenticationError(f"Device flow error: {error}")
        else:
            raise FailedAuthenticationError("Unexpected error during device flow login")


def get_current_user() -> dict:
    """Fetch current authenticated user info from AIoD API."""
    if not config.access_token:
        raise NotAuthenticatedError("No access token set. Please login first.")

    response = requests.get(
        f"{config.api_base_url}authorization_test",
        headers={"Authorization": f"Bearer {config.access_token}"},
    )

    if response.status_code == 401:
        raise NotAuthenticatedError("Invalid or expired token.")

    return response.json()
