import requests

from aiod_sdk.endpoints.endpoint import EndpointBase


class AuthorizationTest(EndpointBase):
    name = "authorization_test"

    @classmethod
    def test(cls) -> requests.Response:
        url = cls.api_base_url + cls.name
        res = requests.get(url)
        return res
