from http import HTTPStatus

import aiohttp
import asyncio
import requests

import pandas as pd
from typing import Literal
from functools import partial

from aiod.authentication.authentication import get_token, _get_auth_headers
from aiod.calls.urls import (
    url_to_get_asset,
    url_to_get_content,
    url_to_get_list,
    url_to_get_list_from_platform,
    url_to_get_asset_from_platform,
    url_to_resource_counts,
    url_to_search,
    server_url,
)
from aiod.calls.utils import format_response, wrap_calls, ServerError


def get_any_asset(
    identifier: str,
    data_format: Literal["pandas", "json"] = "pandas",
) -> dict | pd.Series:
    """Get any asset on AI-on-Demand by identifier.

    Parameters
    ----------
    identifier:
        The identifier of the asset, e.g., `'data_...'`.
    data_format:
        The format of the value to be returned.

    Returns
    -------
    :
        All metadata of the asset.

    Raises
    ------
    KeyError
        If the asset cannot be found.
    """
    res = requests.get(
        server_url() + f"assets/{identifier}",
        headers=_get_auth_headers(required=False),
    )

    if res.status_code == HTTPStatus.NOT_FOUND:
        raise KeyError(f"Asset with identifier {identifier!r} not found.")
    if res.status_code != HTTPStatus.OK:
        raise ServerError(res)
    return format_response(res.json(), data_format)


def get_list(
    *,
    asset_type: str,
    platform: str | None = None,
    offset: int = 0,
    limit: int = 10,
    version: str | None = None,
    data_format: Literal["pandas", "json"] = "pandas",
) -> pd.DataFrame | list[dict]:
    """Retrieve a list of ASSET_TYPE from the catalogue.

    All parameters must be specified by name.

    Parameters
    ----------
    platform
        Return metadata of ASSET_TYPE assets of this platform (default is None).
    offset
        The offset for pagination (default is 0).
    limit
        The maximum number of items to retrieve (default is 10).
    version
        The version of the endpoint (default is None).
    data_format
        The desired format for the response (default is "pandas").
        For "json" formats, the returned type is a json decoded type, i.e. in this case a list of dicts.

    Returns
    -------
    :
        The retrieved metadata in the specified format.
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
    identifier: str,
    version: str | None = None,
) -> requests.Response:
    """Delete ASSET_TYPE from the catalogue.

    All parameters must be specified by name.

    Parameters
    ----------
    version
        The version of the endpoint (default is None).

    Returns
    -------
    :
        The server response.
    """
    url = url_to_get_asset(asset_type, identifier, version)
    res = requests.delete(url, headers=get_token().headers)
    if res.status_code == HTTPStatus.NOT_FOUND and "not found" in res.json().get(
        "detail"
    ):
        raise KeyError(f"No {asset_type} with identifier {identifier!r} found.")
    return res


def put_asset(
    *,
    asset_type: str,
    identifier: str,
    metadata: dict,
    version: str | None = None,
) -> requests.Response:
    """Replace a ASSET_TYPE in catalogue.

    All parameters must be specified by name.

    Notes
    -----
    Any attribute not specified in `metadata` will be replaced with the default value!
    If you wish to only modify some attributes and keep the values of others, make sure
    to provide _all_ asset metadata.

    Parameters
    ----------
    identifier
        The identifier of the asset whose metadata to replace.
    metadata
        A dictionary with for each attribute a value.
    version
        If provided, use this version of the REST API instead of `config.version`.

    Returns
    -------
    :
        The server response.

    Raises
    ------
        KeyError if the identifier is not known by the server.
    """
    url = url_to_get_asset(asset_type, identifier, version)
    res = requests.put(url, headers=get_token().headers, json=metadata)
    if res.status_code == HTTPStatus.NOT_FOUND and "not found" in res.json().get(
        "detail"
    ):
        raise KeyError(f"No {asset_type} with identifier {identifier!r} found.")
    return res


def patch_asset(
    *,
    asset_type: str,
    identifier: str,
    metadata: dict,
    version: str | None = None,
) -> requests.Response:
    """Update an ASSET_TYPE in catalogue.

    All parameters must be specified by name.

    Notes
    -----
    This is a best-effort implementation, but is not yet officially supported by the server.

    Parameters
    ----------
    identifier
        The identifier of the asset whose metadata to replace.
    metadata
        A dictionary with for each attribute a value.
    version
        If provided, use this version of the REST API instead of `config.version`.

    Returns
    -------
    :
        The server response.

    Raises
    ------
        KeyError if the identifier is not known by the server.
    """
    url = url_to_get_asset(asset_type, identifier, version)

    asset = get_asset(
        identifier, asset_type=asset_type, version=version, data_format="json"
    )
    del asset["aiod_entry"]
    for attribute, value in metadata.items():
        if attribute not in asset:
            msg = (
                f"Attribute {attribute!r} not available for {asset_type} {identifier}."
            )
            raise AttributeError(msg)
        if not isinstance(value, type(asset[attribute])):
            msg = (
                f"Value {value!r} for attribute {attribute!r} does "
                f"not match expected type {type(asset[attribute])}, is {type(value)}."
            )
            raise TypeError(msg)
        asset[attribute] = value

    res = requests.put(url, headers=get_token().headers, json=asset)
    if res.status_code == HTTPStatus.NOT_FOUND and "not found" in res.json().get(
        "detail"
    ):
        raise KeyError(f"No {asset_type} with identifier {identifier!r} found.")
    return res


def post_asset(
    *,
    asset_type: str,
    metadata: dict,
    version: str | None = None,
) -> str | requests.Response:
    """Register ASSET_TYPE in catalogue.

    All parameters must be specified by name.

    Parameters
    ----------
    metadata
        A dictionary with for each attribute a value.
    version
        If provided, use this version of the REST API instead of `config.version`.

    Returns
    -------
    identifier: str
        if the asset is registered successfully
    error response: requests.Response
        error response, if it failed to register successfully
    """
    url = f"{server_url(version)}{asset_type}"
    res = requests.post(url, headers=get_token().headers, json=metadata)
    if res.status_code == HTTPStatus.OK:
        return res.json()["identifier"]
    return res


def counts(
    *, asset_type: str, version: str | None = None, per_platform: bool = False
) -> int | dict[str, int]:
    """Retrieve the number of ASSET_TYPE assets in the metadata catalogue.

    All parameters must be specified by name.

    Parameters
    ----------
    version
        The version of the endpoint (default is None).
    per_platform
        Whether to list counts per platform (default is False).

    Returns
    -------
    int | dict[str, int]
        The number ASSET_TYPE assets in the metadata catalogue.
        If the parameter per_platform is True,
        it returns a dictionary with platform names as keys
        and the number of ASSET_TYPE assets from that platform as values.
    """
    url = url_to_resource_counts(version, per_platform, asset_type)
    res = requests.get(url)
    return res.json()


def get_asset(
    identifier: str,
    *,
    asset_type: str,
    version: str | None = None,
    data_format: Literal["pandas", "json"] = "pandas",
) -> pd.Series | dict:
    """Retrieve metadata for a specific ASSET_TYPE.

    All parameters except `identifier` must be specified by name.

    Parameters
    ----------
    identifier
        The identifier of the ASSET_TYPE to retrieve.
    version
        The version of the endpoint (default is None).
    data_format
        The desired format for the response (default is "pandas").
        For "json" formats, the returned type is a json decoded type, in this case a dict.

    Returns
    -------
    :
        The retrieved metadata for the specified ASSET_TYPE.

    Raises
    ------
    KeyError
        If the asset cannot be found.
    """
    url = url_to_get_asset(asset_type, identifier, version)
    res = requests.get(url, headers=_get_auth_headers(required=False))
    if res.status_code == HTTPStatus.NOT_FOUND and "not found" in res.json().get(
        "detail"
    ):
        raise KeyError(f"No {asset_type} with identifier {identifier!r} found.")
    resources = format_response(res.json(), data_format)
    return resources


def get_asset_from_platform(
    *,
    platform: str,
    platform_identifier: str,
    asset_type: str,
    version: str | None = None,
    data_format: Literal["pandas", "json"] = "pandas",
) -> pd.Series | dict:
    """Retrieve metadata for a specific ASSET_TYPE identified by the external platform identifier.

    All parameters must be specified by name.

    Parameters
    ----------
    platform
        The platform where the ASSET_TYPE asset is retrieved from.
    platform_identifier
        The identifier under which the ASSET_TYPE is known by the platform.
    version
        The version of the endpoint (default is None).
    data_format
        The desired format for the response (default is "pandas").
        For "json" formats, the returned type is a json decoded type, in this case a dict.

    Returns
    -------
    :
        The retrieved metadata for the specified ASSET_TYPE.
    """
    url = url_to_get_asset_from_platform(
        asset_type, platform, platform_identifier, version
    )
    res = requests.get(url)
    resources = format_response(res.json(), data_format)
    return resources


def get_content(
    *,
    identifier: str,
    asset_type: str,
    distribution_idx: int = 0,
    version: str | None = None,
) -> bytes:
    """Retrieve the data content of a specific ASSET_TYPE.

    All parameters must be specified by name.

    Parameters
    ----------
    identifier
        The identifier of the ASSET_TYPE asset.
    distribution_idx
        The index of a specific distribution from the distribution list (default is 0).
    version
        The version of the endpoint (default is None).

    Returns
    -------
    :
        The data content for the specified ASSET_TYPE.
    """
    url = url_to_get_content(asset_type, identifier, distribution_idx, version)
    res = requests.get(url)
    distribution = res.content
    return distribution


def search(
    query: str,
    *,
    platforms: list[str] | None = None,
    offset: int = 0,
    limit: int = 10,
    search_field: (
        None | Literal["name", "issn", "description_html", "description_plain"]
    ) = None,
    get_all: bool = True,
    version: str | None = None,
    data_format: Literal["pandas", "json"] = "pandas",
    asset_type: str,
) -> pd.DataFrame | list[dict]:
    """Search metadata for ASSET_TYPE type using the Elasticsearch endpoint of the AIoD metadata catalogue.

    All parameters except `query` must be specified by name.

    Parameters
    ----------
    search
        The string to be matched against the search fields.
    platforms
        The platforms to filter the search results.
        If None, results from all platforms will be returned (default is None).
    offset
        The offset for pagination (default is 0).
    limit
        The maximum number of results to retrieve (default is 10).
    search_field
        The specific fields to search within. If None, the query will be matched against all fields (default is None).
    get_all
        If true, a request to the database is made to retrieve all data.
        If false, only the indexed information is returned. (default is True).
    version
        The version of the endpoint to use (default is None).
    data_format
        The desired format for the response (default is "pandas").
        For "json" formats, the returned type is a json decoded type, in this case a list of dict's.

    Returns
    -------
    :
        The retrieved metadata in the specified format.
    """
    url = url_to_search(
        asset_type,
        query,
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
    identifiers: list[str],
    *,
    asset_type: str,
    version: str | None = None,
    data_format: Literal["pandas", "json"] = "pandas",
) -> pd.DataFrame | list[dict]:
    """Asynchronously retrieve metadata for a list of ASSET_TYPE identifiers.

    All parameters except `identifiers` must be specified by name.

    Parameters
    ----------
    identifiers
        The list of identifiers of the ASSET_TYPE to retrieve.
    version
        The version of the endpoint (default is None).
    data_format
        The desired format for the response (default is "pandas").
        For "json" formats, the returned type is a json decoded type, in this case a list of dicts.

    Returns
    -------
    :
        The retrieved metadata for the specified ASSET_TYPE.
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
    """Asynchronously retrieve a list of ASSET_TYPE from the catalogue in batches.

    All parameters must be specified by name.

    Parameters
    ----------
        offset: The offset for pagination (default is 0).
        limit: The maximum number of items to retrieve (default is 10).
        batch_size: The number of items in a a batch.
        version: The version of the endpoint (default is None).
        data_format: The desired format for the response (default is "pandas").
            For "json" formats, the returned type is a json decoded type, in this case a list of dicts.

    Returns
    -------
    :
        The retrieved metadata in the specified format.

    Raises
    ------
    ValueError
        Batch size must be larger than 0.
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


wrap_common_calls = partial(
    wrap_calls,
    calls=[
        get_list,
        counts,
        get_asset,
        post_asset,
        put_asset,
        patch_asset,
        delete_asset,
        get_asset_from_platform,
        get_content,
        get_assets_async,
        get_list_async,
    ],
)
wrap_search_call = partial(wrap_calls, calls=[search])
