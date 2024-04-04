import requests

from aiod_sdk.endpoints.endpoint import EndpointBase


class Counts(EndpointBase):
    """
    Class for retrieving counts of resources.

    This class provides a method to retrieve counts of resources from the counts endpoint.

    Inherits From:
        EndpointBase: Provides base functionality for endpoint interactions.

    Attributes:
        name (str): The name of the counts endpoint.
        latest_version (str): The latest version of the counts endpoint.

    Methods:
        asset_counts(version=None) -> requests.Response:
            Retrieve counts of assets.
    """

    name = "counts"

    @classmethod
    def asset_counts(cls, version: str | None = None) -> requests.Response:
        """
        Retrieve counts of assets.

        This method sends a GET request to the counts endpoint to retrieve counts of assets.

        Parameters:
            version (str | None): The version of the counts endpoint (default is None).

        Returns:
            requests.Response: The response object containing the HTTP response from the server.
        """
        version = version if version is not None else cls.latest_version
        url = cls.api_base_url + cls.name
        if version:
            url += "/" + version

        res = requests.get(url)
        return res
