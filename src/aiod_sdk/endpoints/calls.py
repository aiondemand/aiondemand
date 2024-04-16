import requests
import urllib
import pandas as pd
from typing import Literal, Tuple, Callable
from functools import partial, update_wrapper

from .settings import api_base_url, latest_version


def get_list(
    offset: int = 0,
    limit: int = 10,
    version: str | None = None,
    data_format: Literal["pandas", "dict"] = "pandas",
    asset_type: str | None = None,
) -> pd.DataFrame | dict:
    """
    Retrieve a list of ASSET_TYPE from the catalogue.

    Parameters:
        offset (int): The offset for pagination (default is 0).
        limit (int): The maximum number of items to retrieve (default is 10).
        version (str | None): The version of the endpoint (default is None).
        data_format (Literal["pandas", "dict"]): The desired format for the response (default is "pandas").

    Returns:
        pd.DataFrame | dict: The retrieved metadata in the specified format.
    """
    query = urllib.parse.urlencode({"offset": offset, "limit": limit})
    version = version if version is not None else latest_version
    url = f"{api_base_url}{asset_type}/{version}?{query}"

    res = requests.get(url)
    resources = _format_response(res.json(), data_format)
    return resources


def counts(
    version: str | None = None, detailed: bool = False, asset_type: str | None = None
) -> int:
    """
    Retrieve the counts of ASSET_TYPE.

    Parameters:
        version (str | None): The version of the endpoint (default is None).
        detailed (bool): Whether to retrieve detailed counts (default is False).

    Returns:
        int: The count of ASSET_TYPE.
    """
    query = urllib.parse.urlencode({"detailed": detailed}).lower()
    version = version if version is not None else latest_version
    url = f"{api_base_url}counts/{asset_type}/{version}?{query}"

    res = requests.get(url)
    return res.json()


def get_asset(
    identifier: int,
    version: str | None = None,
    format: Literal["pandas", "dict"] = "pandas",
    asset_type: str | None = None,
) -> pd.Series | dict:
    """
    Retrieve metadata for a specific ASSET_TYPE.

    Parameters:
        identifier (int): The identifier of the ASSET_TYPE to retrieve.
        version (str | None): The version of the endpoint (default is None).
        format (Literal["pandas", "dict"]): The desired format for the response (default is "pandas").

    Returns:
        pd.Series | dict: The retrieved metadata for the specified ASSET_TYPE.
    """
    version = version if version is not None else latest_version
    url = f"{api_base_url}{asset_type}/{version}/{identifier}"

    res = requests.get(url)
    resources = _format_response(res.json(), format)
    return resources


def _wrap_common_calls(asset_type: str, calls: list[Callable]) -> Tuple[Callable, ...]:
    wrapper_list = []
    for wrapped in calls:
        wrapper: Callable = partial(wrapped, asset_type=asset_type)
        wrapper = update_wrapper(wrapper, wrapped)
        wrapper.__doc__ = (
            wrapped.__doc__.replace("ASSET_TYPE", asset_type)
            if wrapped.__doc__ is not None
            else ""
        )
        wrapper_list.append(wrapper)

    return tuple(wrapper_list)


wrap_common_calls = partial(_wrap_common_calls, calls=[get_list, counts, get_asset])


def _format_response(
    response: list | dict, data_format: Literal["pandas", "dict"]
) -> pd.Series | pd.DataFrame | dict:
    """
    Format the response data based on the specified format.

    Parameters:
        response (list | dict): The response data to format.
        data_format (Literal["pandas", "dict"]): The desired format for the response.

    Returns:
        pd.Series | pd.DataFrame | dict: The formatted response data.

    Raises:
        Exception: If the specified format is invalid or not supported.
    """

    if data_format == "pandas":
        if isinstance(response, dict):
            return pd.Series(response)
        if isinstance(response, list):
            return pd.DataFrame(response)
    elif data_format == "dict":
        return response
    else:
        raise Exception(f"Format: {data_format} invalid or not supported.")
