from requests import Response
from aiod_sdk.endpoints.endpoint import Endpoint


class AuthorizationTest(Endpoint):
    name = "authorization_test"

    @classmethod
    def test(cls) -> Response:
        return cls._get(version="")
