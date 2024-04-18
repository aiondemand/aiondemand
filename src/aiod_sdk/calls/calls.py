import aiohttp
import asyncio
import requests

import pandas as pd
from typing import Literal
from functools import partial

from aiod_sdk.calls.utils import (
    url_to_get_asset,
    url_to_get_list,
    url_to_resource_counts,
    format_response,
    wrap_calls,
)


def get_list(
    *,
    asset_type: str,
    offset: int = 0,
    limit: int = 10,
    version: str | None = None,
    data_format: Literal["pandas", "json"] = "pandas",
) -> pd.DataFrame | list:
    """
    Retrieve a list of ASSET_TYPE from the catalogue.

    Parameters (keywords required):
        offset (int): The offset for pagination (default is 0).
        limit (int): The maximum number of items to retrieve (default is 10).
        version (str | None): The version of the endpoint (default is None).
        data_format (Literal["pandas", "json"]): The desired format for the response (default is "pandas").
            For "json" formats, the returned type is a json decoded type, i.e. a dict or a list.

    Returns:
        pd.DataFrame | dict | list: The retrieved metadata in the specified format.
    """
    url = url_to_get_list(asset_type, offset, limit, version)
    res = requests.get(url)
    resources = format_response(res.json(), data_format)
    return resources


def counts(
    *, asset_type: str, version: str | None = None, detailed: bool = False
) -> int:
    """
    Retrieve the counts of ASSET_TYPE.

    Parameters (keywords required):
        version (str | None): The version of the endpoint (default is None).
        detailed (bool): Whether to retrieve detailed counts (default is False).

    Returns:
        int: The count of ASSET_TYPE.
    """

    url = url_to_resource_counts(version, detailed, asset_type)
    res = requests.get(url)
    return res.json()


def get_asset(
    *,
    asset_type: str,
    identifier: int,
    version: str | None = None,
    data_format: Literal["pandas", "json"] = "pandas",
) -> pd.Series | dict:
    """
    Retrieve metadata for a specific ASSET_TYPE.

    Parameters (keywords required):
        identifier (int): The identifier of the ASSET_TYPE to retrieve.
        version (str | None): The version of the endpoint (default is None).
        data_format (Literal["pandas", "json"]): The desired format for the response (default is "pandas").
            For "json" formats, the returned type is a json decoded type, in this case a dict.

    Returns:
        pd.Series | dict: The retrieved metadata for the specified ASSET_TYPE.
    """
    url = url_to_get_asset(asset_type, identifier, version)
    res = requests.get(url)
    resources = format_response(res.json(), data_format)
    return resources


async def get_asset_async(
    *,
    asset_type: str,
    identifiers: list[int],
    version: str | None = None,
    data_format: Literal["pandas", "json"] = "pandas",
) -> pd.DataFrame | list:
    """
    Asynchronously retrieve metadata for a list of ASSET_TYPE identifiers.

    Parameters (keywords required):
        identifiers (list[int]): The list of identifiers of the ASSET_TYPE to retrieve.
        version (str | None): The version of the endpoint (default is None).
        data_format (Literal["pandas", "json"]): The desired format for the response (default is "pandas").
            For "json" formats, the returned type is a json decoded type, i.e. a dict or a list.

    Returns:
        pd.Series | dict: The retrieved metadata for the specified ASSET_TYPE.
    """
    urls = [
        url_to_get_asset(asset_type, identifier, version) for identifier in identifiers
    ]
    response_data = await _fetch_resources(urls)
    resources = format_response(response_data, data_format)
    return resources


async def get_list_async(
    *,
    asset_type: str,
    offset: int = 0,
    limit: int = 100,
    batch_size: int = 10,
    version: str | None = None,
    data_format: Literal["pandas", "json"] = "pandas",
) -> pd.DataFrame | list:
    """
    Asynchronously retrieve a list of ASSET_TYPE from the catalogue in batches.

    Parameters (keywords required):
        offset (int): The offset for pagination (default is 0).
        limit (int): The maximum number of items to retrieve (default is 10).
        batch_size (int): The number of items in a a batch.
        version (str | None): The version of the endpoint (default is None).
        data_format (Literal["pandas", "json"]): The desired format for the response (default is "pandas").
            For "json" formats, the returned type is a json decoded type, in this case a list.

    Returns:
        pd.DataFrame | dict: The retrieved metadata in the specified format.
    """
    if batch_size <= 0:
        raise ValueError(
            "batch_size must be larger than 0, otherwise you can use the synchronous get_list function!"
        )
    current_offset = offset
    next_limit = min(batch_size, limit)
    batches = []
    while current_offset < offset + limit:
        batches.append((current_offset, next_limit))
        current_offset += next_limit
        next_limit = min(batch_size, offset + limit - current_offset)

    urls = [
        url_to_get_list(asset_type, offset, limit, version) for offset, limit in batches
    ]

    response_data = await _fetch_resources(urls)
    flattened_response_data = [
        response for batch in response_data for response in batch
    ]
    resources = format_response(flattened_response_data, data_format)
    return resources


async def _fetch_resources(urls) -> dict:
    async def _fetch_data(session, url) -> dict:
        async with session.get(url) as response:
            return await response.json()

    async with aiohttp.ClientSession() as session:
        tasks = [_fetch_data(session, url) for url in urls]
        response_data = await asyncio.gather(*tasks)
    return response_data


wrap_common_calls = partial(wrap_calls, calls=[get_list, counts, get_asset])
wrap_common_async_calls = partial(wrap_calls, calls=[get_asset_async, get_list_async])
