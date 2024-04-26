import urllib

from typing import Literal

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


def url_to_search(
    asset_type: str,
    search_query: str,
    platforms: list[str] | None = None,
    offset: int = 0,
    limit: int = 10,
    search_fields: (
        None | Literal["name", "issn", "description_html", "description_plain"]
    ) = None,
    get_all: bool = True,
    version: str | None = None,
) -> str:
    query_params = {
        key: value
        for key, value in locals().items()
        if value is not None and value != "" and key not in ["version", "asset_type"]
    }
    query = urllib.parse.urlencode(query_params, doseq=True).lower()
    version = version if version is not None else latest_version
    url = f"{api_base_url}search/{asset_type}/{version}?{query}"
    return url


def url_to_resource_counts(
    version: str | None = None,
    per_platform: bool = False,
    asset_type: str | None = None,
) -> str:
    query = urllib.parse.urlencode({"detailed": per_platform}).lower()
    version = version if version is not None else latest_version
    url = f"{api_base_url}counts/{asset_type}/{version}?{query}"
    return url


def url_to_get_content(
    asset_type: str,
    identifier: int,
    distribution_idx: int,
    version: str | None = None,
) -> str:
    version = version if version is not None else latest_version
    url = f"{api_base_url}{asset_type}/{version}/{identifier}/content"
    url += f"/{distribution_idx}" if distribution_idx else ""
    return url


def url_to_get_list_from_platform(
    asset_type: str,
    platform: str,
    offset: int = 0,
    limit: int = 10,
    version: str | None = None,
) -> str:

    query = urllib.parse.urlencode({"offset": offset, "limit": limit})
    version = version if version is not None else latest_version

    url = f"{api_base_url}platforms/{platform}/{asset_type}/{version}?{query}"
    return url


def url_to_get_asset_from_platform(
    asset_type: str,
    platform: str,
    platform_identifier: str,
    version: str | None = None,
) -> str:

    version = version if version is not None else latest_version

    url = f"{api_base_url}platforms/{platform}/{asset_type}/{version}/{platform_identifier}"
    return url
