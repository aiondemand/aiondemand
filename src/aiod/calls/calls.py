import aiohttp
import asyncio
import requests

import pandas as pd
from typing import Literal, Callable
from functools import partial

from aiod import config
from aiod.calls.urls import (
    url_to_get_asset,
    url_to_put_asset,
    url_to_post_asset,
    url_to_delete_asset,
    url_to_get_content,
    url_to_get_list,
    url_to_get_list_from_platform,
    url_to_get_asset_from_platform,
    url_to_resource_counts,
    url_to_search,
)
from aiod.calls.utils import format_response, wrap_calls


def get_list(
    *,
    asset_type: str,
    platform: str | None = None,
    offset: int = 0,
    limit: int = 10,
    version: str | None = None,
    data_format: Literal["pandas", "json"] = "pandas",
) -> pd.DataFrame | list[dict]:
    """
    Retrieve a list of ASSET_TYPE from the catalogue.

    Parameters (keywords required):
        platform (str | None): Return metadata of ASSET_TYPE assets of this platform (default is None).
        offset (int): The offset for pagination (default is 0).
        limit (int): The maximum number of items to retrieve (default is 10).
        version (str | None): The version of the endpoint (default is None).
        data_format (Literal["pandas", "json"]): The desired format for the response (default is "pandas").
            For "json" formats, the returned type is a json decoded type, i.e. in this case a list of dict's.

    Returns:
        pd.DataFrame | list[dict]: The retrieved metadata in the specified format.
    """
    url = (
        url_to_get_list_from_platform(asset_type, platform, offset, limit, version)
        if platform is not None
        else url_to_get_list(asset_type, offset, limit, version)
    )
    res = requests.get(url)
    resources = format_response(res.json(), data_format)
    return resources


def delete_asset(
    *,
    asset_type: str,
    identifier: int,
    version: str | None = None,
) -> requests.Response:
    """
    Delete ASSET_TYPE from the catalogue.

    Parameters (keywords required):

        version (str | None): The version of the endpoint (default is None).
        data_format (Literal["pandas", "json"]): The desired format for the response (default is "pandas").
            For "json" formats, the returned type is a json decoded type, i.e. in this case a list of dict's.
    """
    url = url_to_delete_asset(asset_type, identifier, version)
    headers = {"Authorization": f"Bearer {config.access_token}"}
    res = requests.delete(url, headers=headers)

    return res


def put_asset(
    *,
    asset_type: str,
    identifier: int,
    metadata: dict,
    version: str | None = None,
) -> requests.Response:
    """
    Delete ASSET_TYPE from the catalogue.

    Parameters (keywords required):

        version (str | None): The version of the endpoint (default is None).
        data_format (Literal["pandas", "json"]): The desired format for the response (default is "pandas").
            For "json" formats, the returned type is a json decoded type, i.e. in this case a list of dict's.
    """
    url = url_to_put_asset(asset_type, identifier, version)
    headers = {"Authorization": f"Bearer {config.access_token}"}
    res = requests.put(url, headers=headers, data=metadata)

    return res


def post_asset(
    *,
    asset_type: str,
    metadata: dict,
    version: str | None = None,
) -> requests.Response:
    """
    Delete ASSET_TYPE from the catalogue.

    Parameters (keywords required):

        version (str | None): The version of the endpoint (default is None).
        data_format (Literal["pandas", "json"]): The desired format for the response (default is "pandas").
            For "json" formats, the returned type is a json decoded type, i.e. in this case a list of dict's.
    """
    url = url_to_post_asset(asset_type, version)
    headers = {"Authorization": f"Bearer {config.access_token}"}
    res = requests.post(url, headers=headers, data=metadata)

    return res


def counts(
    *, asset_type: str, version: str | None = None, per_platform: bool = False
) -> int | dict[str, int]:
    """
    Retrieve the number of ASSET_TYPE assets in the metadata catalogue.

    Parameters (keywords required):
        version (str | None): The version of the endpoint (default is None).
        per_platform (bool): Whether to list counts per platform (default is False).

    Returns:
        int | dict[str, int]: The number ASSET_TYPE assets in the metadata catalogue.
            If the parameter per_platform is True, it returns a dict[str, int].
    """

    url = url_to_resource_counts(version, per_platform, asset_type)
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


def get_asset_from_platform(
    *,
    asset_type: str,
    platform: str,
    platform_identifier: str,
    version: str | None = None,
    data_format: Literal["pandas", "json"] = "pandas",
) -> pd.Series | dict:
    """
    Retrieve metadata for a specific ASSET_TYPE identified by the external platform identifier.

    Parameters (keywords required):
        platform (str): The platform where the ASSET_TYPE asset is retrieved from.
        platform_identifier (str): The identifier under which the ASSET_TYPE is known by the platform.
        version (str | None): The version of the endpoint (default is None).
        data_format (Literal["pandas", "json"]): The desired format for the response (default is "pandas").
            For "json" formats, the returned type is a json decoded type, in this case a dict.

    Returns:
        pd.Series | dict: The retrieved metadata for the specified ASSET_TYPE.
    """
    url = url_to_get_asset_from_platform(
        asset_type, platform, platform_identifier, version
    )
    res = requests.get(url)
    resources = format_response(res.json(), data_format)
    return resources


def get_content(
    *,
    asset_type: str,
    identifier: int,
    distribution_idx: int = 0,
    version: str | None = None,
) -> bytes:
    """
    Retrieve the data content of a specific ASSET_TYPE.

    Parameters (keywords required):
        identifier (int): The identifier of the ASSET_TYPE asset.
        distribution_idx (int): The index of a specific distribution from the distribution list (default is 0).
        version (str | None): The version of the endpoint (default is None).

    Returns:
        bytes: The data content for the specified ASSET_TYPE.
    """
    url = url_to_get_content(asset_type, identifier, distribution_idx, version)
    res = requests.get(url)
    distribution = res.content
    return distribution


def search(
    *,
    asset_type: str,
    search_query: str,
    platforms: list[str] | None = None,
    offset: int = 0,
    limit: int = 10,
    search_field: (
        None | Literal["name", "issn", "description_html", "description_plain"]
    ) = None,
    get_all: bool = True,
    version: str | None = None,
    data_format: Literal["pandas", "json"] = "pandas",
) -> pd.DataFrame | list[dict]:
    """
    Search metadata for ASSET_TYPE type using the Elasticsearch endpoint of the AIoD metadata catalogue.

    Parameters (keywords required):
        search_query (str): The string to be matched against the search fields.
        platforms (list[str] | None): The platforms to filter the search results.
            If None, results from all platforms will be returned (default is None).
        offset (int): The offset for pagination (default is 0).
        limit (int): The maximum number of results to retrieve (default is 10).
        search_field (None | Literal["name", "issn", "description_html", "description_plain"]):
            The specific fields to search within. If None, the query will be matched against all fields (default is None).
        get_all (bool): If true, a request to the database is made to retrieve all data.
            If false, only the indexed information is returned. (default is True).
        version (str | None): The version of the endpoint to use (default is None).
        data_format (Literal["pandas", "json"]): The desired format for the response (default is "pandas").
            For "json" formats, the returned type is a json decoded type, in this case a list of dict's.

    Returns:
        pd.DataFrame | list[dict]: The retrieved metadata in the specified format.
    """

    url = url_to_search(
        asset_type,
        search_query,
        platforms,
        offset,
        limit,
        search_field,
        get_all,
        version,
    )
    res = requests.get(url)
    resources = format_response(res.json()["resources"], data_format)
    return resources


async def get_assets_async(
    *,
    asset_type: str,
    identifiers: list[int],
    version: str | None = None,
    data_format: Literal["pandas", "json"] = "pandas",
) -> pd.DataFrame | list[dict]:
    """
    Asynchronously retrieve metadata for a list of ASSET_TYPE identifiers.

    Parameters (keywords required):
        identifiers (list[int]): The list of identifiers of the ASSET_TYPE to retrieve.
        version (str | None): The version of the endpoint (default is None).
        data_format (Literal["pandas", "json"]): The desired format for the response (default is "pandas").
            For "json" formats, the returned type is a json decoded type, in this case a list of dict's.

    Returns:
        pd.DataFrame | list[dict]: The retrieved metadata for the specified ASSET_TYPE.
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
) -> pd.DataFrame | list[dict]:
    """
    Asynchronously retrieve a list of ASSET_TYPE from the catalogue in batches.

    Parameters (keywords required):
        offset (int): The offset for pagination (default is 0).
        limit (int): The maximum number of items to retrieve (default is 10).
        batch_size (int): The number of items in a a batch.
        version (str | None): The version of the endpoint (default is None).
        data_format (Literal["pandas", "json"]): The desired format for the response (default is "pandas").
            For "json" formats, the returned type is a json decoded type, in this case a list of dict's.

    Returns:
        pd.DataFrame | list[dict]: The retrieved metadata in the specified format.
    """
    if batch_size <= 0:
        raise ValueError(
            "batch_size must be larger than 0, otherwise you can use the synchronous get_list function!"
        )

    offsets = range(offset, offset + limit, batch_size)
    last_batch_size = (limit % batch_size) or batch_size
    batch_sizes = [batch_size] * (len(offsets) - 1) + [last_batch_size]

    urls = [
        url_to_get_list(asset_type, offset, limit, version)
        for offset, limit in zip(offsets, batch_sizes)
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


wrap_common_calls: Callable = partial(
    wrap_calls,
    calls=[
        get_list,
        counts,
        get_asset,
        post_asset,
        put_asset,
        delete_asset,
        get_asset_from_platform,
        get_content,
        get_assets_async,
        get_list_async,
    ],
)
wrap_search_call: Callable = partial(wrap_calls, calls=[search])
