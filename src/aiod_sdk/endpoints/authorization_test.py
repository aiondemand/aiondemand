import requests

from aiod_sdk.endpoints.endpoint import EndpointBase


class AuthorizationTest(EndpointBase):
    """
    Class for testing authorization functionality.

    This class provides a method for testing authorization functionality by sending a GET request to the authorization_test endpoint.

    Attributes:
        name (str): The name of the authorization_test endpoint.

    Methods:
        test() -> requests.Response:
            Send a GET request to the authorization_test endpoint and return the response.

    """

    name = "authorization_test"

    @classmethod
    def test(cls) -> requests.Response:
        """
        Send a test request to the authorization_test endpoint.

        This method sends a GET request to the authorization_test endpoint and returns the response.

        Returns:
            requests.Response: The response object containing the HTTP response from the server.
        """

        url = cls.api_base_url + cls.name
        res = requests.get(url)
        return res
