import asyncio
import pytest
import responses

from aioresponses import aioresponses
from typing import Callable

import aiod_sdk as aiod

from aiod_sdk.config.settings import API_BASE_URL, LATEST_VERSION


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


@pytest.fixture(params=asset_names)
def asset_name(request):
    return request.param


def test_endpoints_are_created(asset_name: str):

    asset = getattr(aiod, asset_name)
    assert isinstance(getattr(asset, "get_list"), Callable)
    assert isinstance(getattr(asset, "get_asset"), Callable)
    assert isinstance(getattr(asset, "counts"), Callable)
    assert isinstance(getattr(asset, "get_list_async"), Callable)
    assert isinstance(getattr(asset, "get_asset_async"), Callable)


def test_endpoint_get_list(asset_name):
    with responses.RequestsMock() as mocked_requests:
        mocked_requests.add(
            responses.GET,
            API_BASE_URL + f"{asset_name}/" + LATEST_VERSION + "?offset=0&limit=10",
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
            API_BASE_URL
            + "counts/"
            + f"{asset_name}/"
            + LATEST_VERSION
            + "?detailed=false",
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
            API_BASE_URL + f"{asset_name}/" + LATEST_VERSION + "/" + "1",
            body=b'{"resource":"fake_details"}',
            status=200,
        )
        endpoint = getattr(aiod, asset_name)
        metadata = endpoint.get_asset(identifier=1, data_format="dict")

        assert metadata == {"resource": "fake_details"}


def test_endpoint_get_asset_async(asset_name):
    loop = asyncio.get_event_loop()
    with aioresponses() as mocked_responses:
        mocked_responses.get(
            API_BASE_URL + f"{asset_name}/" + LATEST_VERSION + "/" + "1",
            payload={"resource": "fake_details"},
            status=200,
        )
        mocked_responses.get(
            API_BASE_URL + f"{asset_name}/" + LATEST_VERSION + "/" + "3",
            payload={"resource": "fake_details_2"},
            status=200,
        )

        endpoint = getattr(aiod, asset_name)
        metadata = loop.run_until_complete(
            endpoint.get_asset_async(identifiers=[1, 3], data_format="dict")
        )
        assert metadata == [
            {"resource": "fake_details"},
            {"resource": "fake_details_2"},
        ]


def test_endpoint_get_list_async(asset_name):
    loop = asyncio.get_event_loop()
    with aioresponses() as mocked_responses:
        mocked_responses.get(
            API_BASE_URL + f"{asset_name}/" + LATEST_VERSION + "?offset=0&limit=2",
            payload=[{"resource_1": "info"}, {"resource_2": "info"}],
            status=200,
        )
        mocked_responses.get(
            API_BASE_URL + f"{asset_name}/" + LATEST_VERSION + "?offset=2&limit=1",
            payload=[{"resource_3": "info"}],
            status=200,
        )

        endpoint = getattr(aiod, asset_name)
        metadata = loop.run_until_complete(
            endpoint.get_list_async(offset=0, limit=3, batch_size=2, data_format="dict")
        )
        assert metadata == [
            {"resource_1": "info"},
            {"resource_2": "info"},
            {"resource_3": "info"},
        ]
