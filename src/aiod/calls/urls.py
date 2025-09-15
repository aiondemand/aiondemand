import urllib

from typing import Literal
import urllib.parse

from aiod.configuration import config


def url_to_get_asset(
    asset_type: str, identifier: str, version: str | None = None
) -> str:
    base_url = server_url(version)
    url = f"{base_url}{asset_type}/{identifier}"
    return url


def url_to_get_list(
    asset_type: str, offset: int = 0, limit: int = 10, version: str | None = None
) -> str:
    query = urllib.parse.urlencode({"offset": offset, "limit": limit})
    base_url = server_url(version)
    url = f"{base_url}{asset_type}?{query}"
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
    base_url = server_url(version)
    url = f"{base_url}search/{asset_type}?{query}"
    return url


def url_to_resource_counts(
    version: str | None = None,
    per_platform: bool = False,
    asset_type: str | None = None,
) -> str:
    query = urllib.parse.urlencode({"detailed": per_platform}).lower()
    base_url = server_url(version)
    url = f"{base_url}counts/{asset_type}?{query}"
    return url


def url_to_get_content(
    asset_type: str,
    identifier: str,
    distribution_idx: int,
    version: str | None = None,
) -> str:
    base_url = server_url(version)
    url = f"{base_url}{asset_type}/{identifier}/content"
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
    base_url = server_url(version)
    url = f"{base_url}platforms/{platform}/{asset_type}?{query}"
    return url


def url_to_get_asset_from_platform(
    asset_type: str,
    platform: str,
    platform_identifier: str,
    version: str | None = None,
) -> str:
    base_url = server_url(version)
    url = f"{base_url}platforms/{platform}/{asset_type}/{platform_identifier}"
    return url


def server_url(version: str | None = None) -> str:
    version_str = version if version is not None else config.version
    if version_str:
        return f"{config.api_server}{version_str}/"
    return config.api_server
