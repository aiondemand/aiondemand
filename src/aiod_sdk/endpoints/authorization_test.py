import requests
from aiod_sdk import crud_service


class AuthorizationTest:
    endpoint: str = "authorization_test"

    @classmethod
    def authorization_test(cls) -> requests.Response:
        return crud_service.get(cls.endpoint)
