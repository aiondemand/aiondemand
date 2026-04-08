import pytest
import responses
import json
from http import HTTPStatus
import aiod
from aiod.calls.urls import server_url
from aiod.calls.utils import ServerError

@responses.activate
def test_get_list_error_handling():
    asset_name = "datasets"
    responses.add(
        responses.GET,
        f"{server_url()}{asset_name}?offset=0&limit=10",
        json={"detail": "Internal Server Error"},
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )
    with pytest.raises(ServerError):
        aiod.datasets.get_list()

@responses.activate
def test_search_error_handling():
    asset_name = "datasets"
    query = "test"
    responses.add(
        responses.GET,
        f"{server_url()}search/{asset_name}?search_query={query}&offset=0&limit=10&get_all=true",
        json={"resources": [], "detail": "Internal Server Error"},
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )
    with pytest.raises(ServerError):
        aiod.datasets.search(query=query, data_format="json")

@responses.activate
@pytest.mark.usefixtures("valid_refresh_token")
def test_post_asset_success_returns_str():
    asset_name = "datasets"
    identifier = "data_123"
    responses.add(
        responses.POST,
        f"http://not.set/not_set/{asset_name}",
        json={"identifier": identifier},
        status=HTTPStatus.OK,
    )
    res = aiod.datasets.register(metadata={"name": "test"})
    assert isinstance(res, str)
    assert res == identifier

@responses.activate
@pytest.mark.usefixtures("valid_refresh_token")
def test_post_asset_error_raises_server_error():
    asset_name = "datasets"
    responses.add(
        responses.POST,
        f"http://not.set/not_set/{asset_name}",
        json={"detail": "Bad Request"},
        status=HTTPStatus.BAD_REQUEST,
    )
    with pytest.raises(ServerError):
        aiod.datasets.register(metadata={"name": "test"})
