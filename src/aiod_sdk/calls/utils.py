import urllib

import pandas as pd

from functools import partial, update_wrapper
from typing import Callable, Literal, Tuple

from aiod_sdk.config.settings import api_base_url, latest_version


def url_to_get_asset(
    asset_type: str, identifier: int, version: str | None = None
) -> str:

    version = version if version is not None else latest_version
    url = f"{api_base_url}{asset_type}/{version}/{identifier}"
    return url


def url_to_get_list(
    asset_type: str, offset: int = 0, limit: int = 10, version: str | None = None
) -> str:

    query = urllib.parse.urlencode({"offset": offset, "limit": limit})
    version = version if version is not None else latest_version
    url = f"{api_base_url}{asset_type}/{version}?{query}"
    return url


def url_to_resource_counts(
    version: str | None = None, detailed: bool = False, asset_type: str | None = None
) -> str:
    query = urllib.parse.urlencode({"detailed": detailed}).lower()
    version = version if version is not None else latest_version
    url = f"{api_base_url}counts/{asset_type}/{version}?{query}"
    return url


def format_response(
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


def wrap_calls(asset_type: str, calls: list[Callable]) -> Tuple[Callable, ...]:
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
