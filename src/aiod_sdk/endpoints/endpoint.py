import abc
import requests
import urllib
import pandas as pd
from typing import Literal

API_BASE_URL = "https://api.aiod.eu/"
LATEST_VERSION = "v1"


class EndpointBase(abc.ABC):
    api_base_url: str = API_BASE_URL
    latest_version: str = LATEST_VERSION
    name: str


class Endpoint(EndpointBase, abc.ABC):
    """
    Abstract class for endpoints.

    This class provides base functionality for endpoint interactions.
    """

    @staticmethod
    def _format_response(
        response: list | dict, format: Literal["pandas", "dict"]
    ) -> pd.Series | pd.DataFrame | dict:
        """
        Format the response data based on the specified format.

        Parameters:
            response (list | dict): The response data to format.
            format (Literal["pandas", "dict"]): The desired format for the response.

        Returns:
            pd.Series | pd.DataFrame | dict: The formatted response data.

        Raises:
            Exception: If the specified format is invalid or not supported.
        """

        if format == "pandas":
            if isinstance(response, dict):
                return pd.Series(response)
            if isinstance(response, list):
                return pd.DataFrame(response)
        elif format == "dict":
            return response
        else:
            raise Exception(f"Format: {format} invalid or not supported.")

    @classmethod
    def list(
        cls,
        offset: int = 0,
        limit: int = 10,
        version: str | None = None,
        format: Literal["pandas", "dict"] = "pandas",
    ) -> pd.DataFrame | dict:
        """
        Retrieve a list of metadata from the catalogue.

        Parameters:
            offset (int): The offset for pagination (default is 0).
            limit (int): The maximum number of items to retrieve (default is 10).
            version (str | None): The version of the endpoint (default is None).
            format (Literal["pandas", "dict"]): The desired format for the response (default is "pandas").

        Returns:
            pd.DataFrame | dict: The retrieved metadata in the specified format.
        """
        query = urllib.parse.urlencode({"offset": offset, "limit": limit})
        version = version if version is not None else cls.latest_version
        url = f"{cls.api_base_url}{cls.name}/{version}?{query}"

        res = requests.get(url)
        resources = cls._format_response(res.json(), format)
        return resources

    @classmethod
    def counts(cls, version: str | None = None, detailed: bool = False) -> int:
        """
        Retrieve the count of resources.

        Parameters:
            version (str | None): The version of the endpoint (default is None).
            detailed (bool): Whether to retrieve detailed counts (default is False).

        Returns:
            int: The count of resources.
        """
        query = urllib.parse.urlencode({"detailed": detailed}).lower()
        version = version if version is not None else cls.latest_version
        url = f"{cls.api_base_url}counts/{cls.name}/{version}?{query}"

        res = requests.get(url)
        return res.json()

    @classmethod
    def get(
        cls,
        identifier: int,
        version: str | None = None,
        format: Literal["pandas", "dict"] = "pandas",
    ) -> pd.Series | dict:
        """
        Retrieve metadata for a specific resource.

        Parameters:
            identifier (int): The identifier of the resource to retrieve.
            version (str | None): The version of the endpoint (default is None).
            format (Literal["pandas", "dict"]): The desired format for the response (default is "pandas").

        Returns:
            pd.Series | dict: The retrieved metadata for the specified resource.
        """
        version = version if version is not None else cls.latest_version
        url = f"{cls.api_base_url}{cls.name}/{version}/{identifier}"

        res = requests.get(url)
        resources = cls._format_response(res.json(), format)
        return resources

    @classmethod
    def post(cls, endpoint: str):
        pass

    @classmethod
    def put(cls, endpoint: str):
        pass

    @classmethod
    def delete(cls, endpoint: str):
        pass
