from requests import Response
from aiod_sdk.endpoints.endpoint import Endpoint


class Counts(Endpoint):
    name = "counts"

    @classmethod
    def asset_counts(cls, version: str | None = None) -> Response:
        return cls._get(version)
