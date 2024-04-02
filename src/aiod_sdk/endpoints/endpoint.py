import abc
import requests
from urllib.parse import urljoin

API_BASE_URL = "https://api.aiod.eu/"
LATEST_VERSION = "v1"


class EndpointBase(abc.ABC):
    api_base_url: str = API_BASE_URL
    latest_version: str = LATEST_VERSION
    name: str


class Endpoint(EndpointBase, abc.ABC):
    @classmethod
    def _get(cls, version: str | None = None) -> requests.Response:
        version = version if version is not None else cls.latest_version
        url = urljoin(cls.api_base_url, cls.name)
        if version:
            url = urljoin(url + "/", version)

        res = requests.get(url)

        return res

    @classmethod
    def post(cls, endpoint: str):
        pass

    @classmethod
    def put(cls, endpoint: str):
        pass

    @classmethod
    def delete(cls, endpoint: str):
        pass
