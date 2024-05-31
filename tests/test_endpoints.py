import asyncio
import pytest
import responses

from aioresponses import aioresponses
from pathlib import Path
from typing import Callable

import aiod

from aiod.configuration import config

resources_path = Path(__file__).parent / "resources"


asset_names = [
    "case_studies",
    "computational_assets",
    "contacts",
    "datasets",
    "educational_resources",
    "events",
    "experiments",
    "ml_models",
    "news",
    "organisations",
    "persons",
    "platforms",
    "projects",
    "publications",
    "services",
    "teams",
]

assets_with_search = [
    "datasets",
    "events",
    "experiments",
    "ml_models",
    "news",
    "organisations",
    "projects",
    "publications",
    "services",
]


@pytest.fixture(params=asset_names)
def asset_name(request):
    return request.param


@pytest.fixture(params=assets_with_search)
def asset_with_search(request):
    return request.param


def test_common_endpoints_are_created(asset_name: str):
    asset = getattr(aiod, asset_name)
    assert isinstance(getattr(asset, "get_list"), Callable)
    assert isinstance(getattr(asset, "counts"), Callable)
    assert isinstance(getattr(asset, "get_asset"), Callable)
    assert isinstance(getattr(asset, "get_asset_from_platform"), Callable)
    assert isinstance(getattr(asset, "get_content"), Callable)
    assert isinstance(getattr(asset, "get_list_async"), Callable)
    assert isinstance(getattr(asset, "get_assets_async"), Callable)


def test_search_endpoints_are_created(asset_with_search: str):
    asset = getattr(aiod, asset_with_search)
    assert isinstance(getattr(asset, "search"), Callable)


def test_endpoint_get_list(asset_name):
    with responses.RequestsMock() as mocked_requests:
        mocked_requests.add(
            responses.GET,
            f"{config.api_base_url}{asset_name}/{config.version}?offset=0&limit=10",
            body=b'[{"resource_1": "info"},{"resource_2": "info"}]',
            status=200,
        )
        endpoint = getattr(aiod, asset_name)
        metadata_list = endpoint.get_list()

        assert len(metadata_list) == 2


def test_endpoint_counts(asset_name):
    with responses.RequestsMock() as mocked_requests:
        mocked_requests.add(
            responses.GET,
            f"{config.api_base_url}counts/{asset_name}/{config.version}?detailed=false",
            body=b"2",
            status=200,
        )
        endpoint = getattr(aiod, asset_name)
        counts = endpoint.counts()

        assert counts == 2


def test_endpoint_get_asset(asset_name):
    with responses.RequestsMock() as mocked_requests:
        mocked_requests.add(
            responses.GET,
            f"{config.api_base_url}{asset_name}/{config.version}/1",
            body=b'{"resource":"fake_details"}',
            status=200,
        )
        endpoint = getattr(aiod, asset_name)
        metadata = endpoint.get_asset(identifier=1, data_format="json")

        assert metadata == {"resource": "fake_details"}


def test_endpoint_get_list_from_platform(asset_name):
    platform_name = "zenodo"
    with responses.RequestsMock() as mocked_requests:
        mocked_requests.add(
            responses.GET,
            f"{config.api_base_url}platforms/{platform_name}/{asset_name}/{config.version}?offset=0&limit=10",
            body=b'[{"resource_1": "info"},{"resource_2": "info"}]',
            status=200,
        )
        endpoint = getattr(aiod, asset_name)
        metadata_list = endpoint.get_list(platform=platform_name)

        assert len(metadata_list) == 2


def test_endpoint_get_asset_from_platform(asset_name):
    platform_name = "zenodo"
    platform_identifier = "zenodo.org:1000"
    with responses.RequestsMock() as mocked_requests:
        mocked_requests.add(
            responses.GET,
            f"{config.api_base_url}platforms/{platform_name}/{asset_name}/{config.version}/{platform_identifier}",
            body=b'{"resource":"fake_details"}',
            status=200,
        )
        endpoint = getattr(aiod, asset_name)
        metadata = endpoint.get_asset_from_platform(
            platform=platform_name,
            platform_identifier=platform_identifier,
            data_format="json",
        )

        assert metadata == {"resource": "fake_details"}


def test_get_content(asset_name):
    with responses.RequestsMock() as mocked_requests:
        with open(resources_path / "content.csv", "r") as f:
            res_body = f.read()
        mocked_requests.add(
            responses.GET,
            f"{config.api_base_url}{asset_name}/{config.version}/1/content",
            body=res_body,
            status=200,
        )
        endpoint = getattr(aiod, asset_name)
        content = endpoint.get_content(identifier=1)

        assert content == b"a,b,c\n1,2,3"


def test_get_content_with_distribution_idx(asset_name):
    with responses.RequestsMock() as mocked_requests:
        with open(resources_path / "content.csv", "r") as f:
            res_body = f.read()
        mocked_requests.add(
            responses.GET,
            f"{config.api_base_url}{asset_name}/{config.version}/1/content/2",
            body=res_body,
            status=200,
        )
        endpoint = getattr(aiod, asset_name)
        content = endpoint.get_content(identifier=1, distribution_idx=2)

        assert content == b"a,b,c\n1,2,3"


def test_search(asset_with_search):
    search_query = "my query"
    search_field = "name"
    platforms = ["aiod", "openml"]
    get_all = True

    query = (
        f"?search_query={search_query.replace(' ', '+')}&platforms={platforms[0]}"
        f"&platforms={platforms[1]}&offset=0&limit=10&search_fields={search_field}&get_all=true"
    )
    with responses.RequestsMock() as mocked_requests:
        mocked_requests.add(
            responses.GET,
            f"{config.api_base_url}search/{asset_with_search}/{config.version}{query}",
            body=b'{"total_hits": 2,"resources": [{"resource_1": "info"},{"resource_2": "info"}],"limit": 10,"offset": 0}',
            status=200,
        )
        endpoint = getattr(aiod, asset_with_search)
        metadata_list = endpoint.search(
            search_query=search_query,
            search_field=search_field,
            platforms=platforms,
            get_all=get_all,
            data_format="json",
        )

        assert len(metadata_list) == 2
        assert metadata_list == [{"resource_1": "info"}, {"resource_2": "info"}]


def test_endpoint_get_asset_async(asset_name):
    loop = asyncio.get_event_loop()
    with aioresponses() as mocked_responses:
        mocked_responses.get(
            f"{config.api_base_url}{asset_name}/{config.version}/1",
            payload={"resource": "fake_details"},
            status=200,
        )
        mocked_responses.get(
            config.api_base_url + f"{asset_name}/" + config.version + "/" + "3",
            payload={"resource": "fake_details_2"},
            status=200,
        )

        endpoint = getattr(aiod, asset_name)
        metadata = loop.run_until_complete(
            endpoint.get_assets_async(identifiers=[1, 3], data_format="json")
        )
        assert metadata == [
            {"resource": "fake_details"},
            {"resource": "fake_details_2"},
        ]


def test_endpoint_get_list_async(asset_name):
    loop = asyncio.get_event_loop()
    with aioresponses() as mocked_responses:
        mocked_responses.get(
            f"{config.api_base_url}{asset_name}/{config.version}?offset=0&limit=2",
            payload=[{"resource_1": "info"}, {"resource_2": "info"}],
            status=200,
        )
        mocked_responses.get(
            f"{config.api_base_url}{asset_name}/{config.version}?offset=2&limit=1",
            payload=[{"resource_3": "info"}],
            status=200,
        )

        endpoint = getattr(aiod, asset_name)
        metadata = loop.run_until_complete(
            endpoint.get_list_async(offset=0, limit=3, batch_size=2, data_format="json")
        )
        assert metadata == [
            {"resource_1": "info"},
            {"resource_2": "info"},
            {"resource_3": "info"},
        ]
