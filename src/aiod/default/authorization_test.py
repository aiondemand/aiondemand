import requests

from aiod.config.settings import api_base_url


def test() -> requests.Response:
    """
    Send a test request to the authorization_test endpoint.

    This method sends a GET request to the authorization_test endpoint and returns the response.

    Returns:
        requests.Response: The response object containing the HTTP response from the server.
    """

    url = api_base_url + "authorization_test"
    res = requests.get(url)
    return res
