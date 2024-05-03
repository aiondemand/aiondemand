import os
from keycloak import KeycloakOpenID

from aiod.config.config import KEYCLOAK_CONFIG


client_secret = os.getenv("KEYCLOAK_CLIENT_SECRET")

keycloak_openid = KeycloakOpenID(
    server_url=KEYCLOAK_CONFIG.get("server_url"),
    client_id=KEYCLOAK_CONFIG.get("client_id"),
    client_secret_key=client_secret,
    realm_name=KEYCLOAK_CONFIG.get("realm"),
    verify=True,
)


def authenticate() -> None:
    username = os.getenv("KEYCLOAK_USERNAME")
    password = os.getenv("KEYCLOAK_PASSWORD")
    if username is None or password is None:
        raise Exception(
            "User credentials not properly set in the environment variables"
        )
    token = keycloak_openid.token(username, password)

    if not token:
        raise Exception("Token error!")
    os.environ["ACCESS_TOKEN"] = token["access_token"]
    os.environ["REFRESH_TOKEN"] = token["refresh_token"]


def logout() -> None:
    refresh_token = get_refresh_token()
    if refresh_token:
        keycloak_openid.logout(refresh_token)


def get_access_token() -> str | None:
    return os.getenv("ACCESS_TOKEN")


def get_refresh_token() -> str | None:
    return os.getenv("REFRESH_TOKEN")
