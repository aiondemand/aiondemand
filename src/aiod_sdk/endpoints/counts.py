import requests

from aiod_sdk.endpoints.endpoint import EndpointBase


class Counts(EndpointBase):
    name = "counts"

    @classmethod
    def asset_counts(cls, version: str | None = None) -> requests.Response:
        version = version if version is not None else cls.latest_version
        url = cls.api_base_url + cls.name
        if version:
            url += "/" + version

        res = requests.get(url)
        return res
