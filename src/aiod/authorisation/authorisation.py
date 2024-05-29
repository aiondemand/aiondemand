import os
from keycloak import KeycloakOpenID

from aiod.config.settings import server_url, client_id, realm

keycloak_openid = KeycloakOpenID(
    server_url=server_url,
    client_id=client_id,
    realm_name=realm,
)


def login(username: str, password: str) -> None:
    """
    Logs in the user with the provided username and password.

    Args:
        username (str): The username of the user.
        password (str): The password of the user.

    Raises:
        MissingCredentialsError: If the username or password is missing.
        MissingTokenError: If Keycloak returns an invalid token.
    """
    if username is None or password is None:
        raise MissingCredentialsError(
            "Username and/or password missing! Please provide your credentials and try again."
        )
    token = keycloak_openid.token(username, password)

    if not token:
        raise MissingTokenError("Keycloak returned an invalid token!")
    os.environ["ACCESS_TOKEN"] = token["access_token"]
    os.environ["REFRESH_TOKEN"] = token["refresh_token"]


def logout() -> None:
    """
    Logs out the current user.

    Raises:
        MissingTokenError: If the stored refresh token is empty.
    """
    refresh_token = get_refresh_token()
    if not refresh_token:
        raise MissingTokenError(
            "The stored refresh token is empty! Please try to login again."
        )

    keycloak_openid.logout(refresh_token)
    os.environ.pop("ACCESS_TOKEN")
    os.environ.pop("REFRESH_TOKEN")


def get_access_token() -> str | None:
    """
    Retrieves the access token.

    Returns:
        str | None: The access token if available, else None.
    """
    return os.getenv("ACCESS_TOKEN")


def get_refresh_token() -> str | None:
    """
    Retrieves the refresh token.

    Returns:
        str | None: The refresh token if available, else None.
    """
    return os.getenv("REFRESH_TOKEN")


class MissingCredentialsError(Exception):
    """Raised when username and/or password is/are missing during login."""


class MissingTokenError(Exception):
    """Raised when a token was failed to be retrieved."""


# from authlib.integrations.requests_client import OAuth2Session

# # Define your client credentials and endpoints

# server_url = "http://keycloak:8080/aiod-auth/"
# realm = "aiod"
# client_id = "aiod-api"  # a private client, used by the backend
# openid_connect_url = (
#     "http://localhost/aiod-auth/realms/aiod/.well-known/openid-configuration"
# )
# scopes = "openid profile roles"
# role = "edit_aiod_resources"

# client_secret = "QJiOGn09eCEfnqAmcPP2l4vMU8grlmVQ"
# # redirect_uri = "http://localhost:8000/callback"
# redirect_uri = ""
# authorization_endpoint = (
#     f"http://localhost/aiod-auth/realms/{realm}/protocol/openid-connect/auth"
# )
# token_endpoint = (
#     f"http://localhost/aiod-auth/realms/{realm}/protocol/openid-connect/token"
# )

# # Create an OAuth2 session
# client = OAuth2Session(client_id, client_secret, redirect_uri=redirect_uri)

# # Step 1: Redirect the user to the authorization URL
# authorization_url, state = client.create_authorization_url(authorization_endpoint)
# print(f"Please go to {authorization_url} and authorize access.")

# # Step 2: Get the authorization response URL from the user
# authorization_response = input("Enter the full callback URL: ")

# # Step 3: Fetch the token using the authorization response
# token = client.fetch_token(
#     token_endpoint,
#     authorization_response=authorization_response,
#     client_secret=client_secret,
# )

# print(f'Access Token: {token["access_token"]}')
