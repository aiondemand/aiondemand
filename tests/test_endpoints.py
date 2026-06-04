import asyncio
import json
from http import HTTPStatus
from pathlib import Path
from typing import Callable

import pytest
from pytest_httpx import HTTPXMock

import aiod
from aiod.calls.urls import server_url
from aiod.calls.utils import EndpointUndefinedError
from aiod.taxonomies import Term

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


def test_endpoint_get_list(asset_name, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method="GET",
        url=f"{server_url()}{asset_name}?offset=0&limit=10",
        content=b'[{"resource_1": "info"},{"resource_2": "info"}]',
    )
    endpoint = getattr(aiod, asset_name)
    metadata_list = endpoint.get_list()

    assert len(metadata_list) == 2


def test_endpoint_counts(asset_name, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method="GET",
        url=f"{server_url()}counts/{asset_name}?detailed=false",
        content=b"2",
    )
    endpoint = getattr(aiod, asset_name)
    counts = endpoint.counts()

    assert counts == 2


def test_endpoint_get_asset(asset_name, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method="GET",
        url=f"{server_url()}{asset_name}/1",
        content=b'{"resource":"fake_details"}',
    )
    endpoint = getattr(aiod, asset_name)
    metadata = endpoint.get_asset(identifier=1, data_format="json")

    assert metadata == {"resource": "fake_details"}


def test_endpoint_update_asset(asset_name, valid_refresh_token, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method="GET",
        url=f"{server_url()}{asset_name}/1",
        json={"name": "fake", "foo": "bar", "aiod_entry": {}},
    )
    httpx_mock.add_response(
        method="PUT",
        url=f"{server_url()}{asset_name}/1",
        match_json={"name": "fake", "foo": "baz"},
        status_code=200,
    )
    endpoint = getattr(aiod, asset_name)
    endpoint.update(identifier=1, metadata=dict(foo="baz"))


def test_endpoint_get_list_from_platform(asset_name, httpx_mock: HTTPXMock):
    platform_name = "zenodo"
    httpx_mock.add_response(
        method="GET",
        url=f"{server_url()}platforms/{platform_name}/{asset_name}?offset=0&limit=10",
        content=b'[{"resource_1": "info"},{"resource_2": "info"}]',
    )
    endpoint = getattr(aiod, asset_name)
    metadata_list = endpoint.get_list(platform=platform_name)

    assert len(metadata_list) == 2


def test_endpoint_get_asset_from_platform(asset_name, httpx_mock: HTTPXMock):
    platform_name = "zenodo"
    platform_identifier = "zenodo.org:1000"
    httpx_mock.add_response(
        method="GET",
        url=f"{server_url()}platforms/{platform_name}/{asset_name}/{platform_identifier}",
        content=b'{"resource":"fake_details"}',
    )
    endpoint = getattr(aiod, asset_name)
    metadata = endpoint.get_asset_from_platform(
        platform=platform_name,
        platform_identifier=platform_identifier,
        data_format="json",
    )

    assert metadata == {"resource": "fake_details"}


def test_get_content(asset_name, httpx_mock: HTTPXMock):
    with open(resources_path / "content.csv", "rb") as f:
        res_body = f.read()
    httpx_mock.add_response(
        method="GET",
        url=f"{server_url()}{asset_name}/1/content",
        content=res_body,
    )
    endpoint = getattr(aiod, asset_name)
    content = endpoint.get_content(identifier=1)

    assert content == b"a,b,c\n1,2,3"


def test_get_content_with_distribution_idx(asset_name, httpx_mock: HTTPXMock):
    with open(resources_path / "content.csv", "rb") as f:
        res_body = f.read()
    httpx_mock.add_response(
        method="GET",
        url=f"{server_url()}{asset_name}/1/content/2",
        content=res_body,
    )
    endpoint = getattr(aiod, asset_name)
    content = endpoint.get_content(identifier=1, distribution_idx=2)

    assert content == b"a,b,c\n1,2,3"


def test_search(asset_with_search, httpx_mock: HTTPXMock):
    search_query = "my query"
    search_field = "name"
    platforms = ["aiod", "openml"]
    get_all = True

    query = (
        f"?search_query={search_query.replace(' ', '+')}&platforms={platforms[0]}"
        f"&platforms={platforms[1]}&offset=0&limit=10&search_fields={search_field}&get_all=true"
    )
    httpx_mock.add_response(
        method="GET",
        url=f"{server_url()}search/{asset_with_search}{query}",
        content=b'{"total_hits": 2,"resources": [{"resource_1": "info"},{"resource_2": "info"}],"limit": 10,"offset": 0}',
    )
    endpoint = getattr(aiod, asset_with_search)
    metadata_list = endpoint.search(
        query=search_query,
        search_field=search_field,
        platforms=platforms,
        get_all=get_all,
        data_format="json",
    )

    assert len(metadata_list) == 2
    assert metadata_list == [{"resource_1": "info"}, {"resource_2": "info"}]


def test_endpoint_get_asset_async(asset_name, httpx_mock: HTTPXMock):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    httpx_mock.add_response(
        method="GET",
        url=f"{server_url()}{asset_name}/1",
        json={"resource": "fake_details"},
    )
    httpx_mock.add_response(
        method="GET",
        url=f"{server_url()}{asset_name}/3",
        json={"resource": "fake_details_2"},
    )

    endpoint = getattr(aiod, asset_name)
    metadata = loop.run_until_complete(
        endpoint.get_assets_async(identifiers=[1, 3], data_format="json")
    )
    assert metadata == [
        {"resource": "fake_details"},
        {"resource": "fake_details_2"},
    ]


def test_endpoint_get_list_async(asset_name, httpx_mock: HTTPXMock):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    httpx_mock.add_response(
        method="GET",
        url=f"{server_url()}{asset_name}?offset=0&limit=2",
        json=[{"resource_1": "info"}, {"resource_2": "info"}],
    )
    httpx_mock.add_response(
        method="GET",
        url=f"{server_url()}{asset_name}?offset=2&limit=1",
        json=[{"resource_3": "info"}],
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


def test_register_asset(asset_name, valid_refresh_token, httpx_mock: HTTPXMock):
    identifier = "data_123412341234123412341234"
    httpx_mock.add_response(
        method="POST",
        url=f"http://not.set/not_set/{asset_name}",
        match_headers={"Authorization": "Bearer valid_access"},
        json={"identifier": identifier},
    )
    module = getattr(aiod, asset_name)
    identifier_ = module.register(metadata=dict(name="Foo"))
    assert identifier_ == identifier


def test_replace_asset(asset_name, valid_refresh_token, httpx_mock: HTTPXMock):
    identifier = "data_123412341234123412341234"
    httpx_mock.add_response(
        method="PUT",
        url=f"http://not.set/not_set/{asset_name}/{identifier}",
        match_headers={"Authorization": "Bearer valid_access"},
        status_code=200,
    )
    module = getattr(aiod, asset_name)
    res = module.replace(identifier=identifier, metadata=dict(description="Foo"))
    assert res.status_code == HTTPStatus.OK


def test_update_asset_incorrect_identifier(asset_name, valid_refresh_token, httpx_mock: HTTPXMock):
    identifier = "data_123412341234123412341234"
    httpx_mock.add_response(
        method="GET",
        url=f"http://not.set/not_set/{asset_name}/{identifier}",
        match_headers={"Authorization": "Bearer valid_access"},
        json={
            "detail": f"{asset_name} '{identifier}' not found in the database.",
            "reference": "8471b0ba3d74436ca645a6c49d0c7d65",
        },
        status_code=HTTPStatus.NOT_FOUND,
    )
    module = getattr(aiod, asset_name)
    with pytest.raises(KeyError) as e:
        module.update(identifier=identifier, metadata=dict(description="Foo"))
    msg = e.value.args[0]
    assert msg.startswith("No") and msg.endswith("found.")


def test_delete_asset(asset_name, valid_refresh_token, httpx_mock: HTTPXMock):
    identifier = "data_123412341234123412341234"
    httpx_mock.add_response(
        method="DELETE",
        url=f"http://not.set/not_set/{asset_name}/{identifier}",
        match_headers={"Authorization": "Bearer valid_access"},
        status_code=200,
    )
    module = getattr(aiod, asset_name)
    res = module.delete(identifier=identifier)
    assert res.status_code == HTTPStatus.OK


def test_delete_asset_incorrect_identifier(asset_name, valid_refresh_token, httpx_mock: HTTPXMock):
    identifier = "data_123412341234123412341234"
    httpx_mock.add_response(
        method="DELETE",
        url=f"http://not.set/not_set/{asset_name}/{identifier}",
        match_headers={"Authorization": "Bearer valid_access"},
        json={
            "detail": f"{asset_name} '{identifier}' not found in the database.",
            "reference": "8471b0ba3d74436ca645a6c49d0c7d65",
        },
        status_code=HTTPStatus.NOT_FOUND,
    )
    module = getattr(aiod, asset_name)
    with pytest.raises(KeyError) as e:
        module.delete(identifier=identifier)
    msg = e.value.args[0]
    assert msg.startswith("No") and msg.endswith("found.")


def test_industrial_sector_taxonomy(httpx_mock: HTTPXMock):
    taxonomy = json.loads((resources_path / "industrial_sectors.json").read_text())
    httpx_mock.add_response(
        method="GET",
        url=f"http://not.set/not_set/industrial_sectors",
        json=taxonomy,
    )

    industrial_sectors = aiod.taxonomies.industrial_sectors.__wrapped__()
    car_industry = Term(
        term="Car Industry", taxonomy="industrial sectors", definition="", subterms=[]
    )
    assert industrial_sectors[0].term == "Manufacturing"
    assert car_industry in industrial_sectors[0].subterms
    assert len(industrial_sectors) == 21


def test_taxonomy_not_found(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method="GET",
        url=f"http://not.set/not_set/industrial_sectors",
        json={"detail": "Not Found"},
        status_code=HTTPStatus.NOT_FOUND,
    )
    with pytest.raises(EndpointUndefinedError):
        # Accessing through __wrapped__ to ensure the cache isn't hit.
        aiod.taxonomies.industrial_sectors.__wrapped__()
