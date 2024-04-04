import pandas as pd
import requests
from typing import Literal

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

    @staticmethod
    def _format_response(
        response: list | dict, format: Literal["pandas", "dict"]
    ) -> pd.DataFrame | dict:
        """
        Format the response data based on the specified format.

        Parameters:
            response (list | dict): The response data to format.
            format (Literal["pandas", "dict"]): The desired format for the response.

        Returns:
            pd.DataFrame | dict: The formatted response data.

        Raises:
            Exception: If the specified format is invalid or not supported.
        """

        if format == "pandas":
            return pd.DataFrame(response)
        elif format == "dict":
            return response
        else:
            raise Exception(f"Format: {format} invalid or not supported.")

    @classmethod
    def asset_counts(
        cls, version: str | None = None, format: Literal["pandas", "dict"] = "pandas"
    ) -> pd.DataFrame | dict:
        """
        Retrieve counts of assets.

        This method sends a GET request to the counts endpoint to retrieve counts of assets.

        Parameters:
            version (str | None): The version of the counts endpoint (default is None).
            format (Literal["pandas", "dict"]): The desired format for the response (default is "pandas").

        Returns:
            pd.DataFrame | dict: Counts as a Pandas data frame or a dictionary.
        """
        version = version if version is not None else cls.latest_version
        url = cls.api_base_url + cls.name
        if version:
            url += "/" + version

        res = requests.get(url)
        counts = cls._format_response(res.json(), format)
        return counts
