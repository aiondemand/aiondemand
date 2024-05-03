import requests

from aiod.config.settings import api_base_url
from aiod.authorisation.authorisation import get_token


def test() -> requests.Response:
    """
    Send a test request to the authorization_test endpoint.

    This method sends a GET request to the authorization_test endpoint and returns the response.

    Returns:
        requests.Response: The response object containing the HTTP response from the server.
    """

    token = get_token()
    headers = {"Authorization": f"Bearer {token['access_token']}"}
    url = api_base_url + "authorization_test"
    res = requests.get(url, headers=headers)
    return res.json()
