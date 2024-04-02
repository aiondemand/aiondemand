import abc
import requests
import urllib

API_BASE_URL = "https://api.aiod.eu/"
LATEST_VERSION = "v1"


class EndpointBase(abc.ABC):
    api_base_url: str = API_BASE_URL
    latest_version: str = LATEST_VERSION
    name: str


class Endpoint(EndpointBase, abc.ABC):
    @classmethod
    def list(
        cls, offset: int = 0, limit: int = 10, version: str | None = None
    ) -> requests.Response:
        query = urllib.parse.urlencode({"offset": offset, "limit": limit})
        version = version if version is not None else cls.latest_version
        url = f"{cls.api_base_url}{cls.name}/{version}?{query}"

        res = requests.get(url)
        return res

    @classmethod
    def counts(
        cls, version: str | None = None, detailed: bool = False
    ) -> requests.Response:
        query = urllib.parse.urlencode({"detailed": detailed}).lower()
        version = version if version is not None else cls.latest_version
        url = f"{cls.api_base_url}counts/{cls.name}/{version}?{query}"

        res = requests.get(url)
        return res

    @classmethod
    def get(cls, identifier: int, version: str | None = None) -> requests.Response:
        version = version if version is not None else cls.latest_version
        url = f"{cls.api_base_url}{cls.name}/{version}/{identifier}"

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
