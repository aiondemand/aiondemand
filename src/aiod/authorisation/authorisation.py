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


def get_token() -> dict:

    username = os.getenv("KEYCLOAK_USERNAME")
    password = os.getenv("KEYCLOAK_PASSWORD")
    if username is None or password is None:
        raise Exception(
            "User credentials not properly set in the environment variables"
        )
    return keycloak_openid.token(username, password)
