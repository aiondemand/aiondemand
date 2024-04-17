import pandas as pd
import requests
from typing import Literal

from aiod_sdk.config.settings import api_base_url, latest_version


def asset_counts(
    version: str | None = None, format: Literal["pandas", "dict"] = "pandas"
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
    version = version if version is not None else latest_version
    url = api_base_url + "counts"
    if version:
        url += "/" + version

    res = requests.get(url)
    counts = _format_response(res.json(), format)
    return counts


def _format_response(
    response: list | dict, data_format: Literal["pandas", "dict"]
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

    if data_format == "pandas":
        return pd.DataFrame(response)
    elif data_format == "dict":
        return response
    else:
        raise Exception(f"Format: {data_format} invalid or not supported.")
