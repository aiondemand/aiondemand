import pytest
from unittest.mock import patch, Mock
from http import HTTPStatus

from aiod.calls.calls import (
    get_any_asset,
    get_asset,
    get_asset_from_platform,
    get_assets_async,
    get_content,
    get_list,
    counts,
    delete_asset,
    get_list_async,
    patch_asset,
    post_asset,
    put_asset,
    search,
)
from aiod.calls.utils import ServerError

class MockResponse:
    def __init__(self, json_data, status_code=200, content=b""):
        self._json = json_data
        self.status_code = status_code
        self.content = content

    def json(self):
        return self._json
    

@patch("aiod.calls.calls.requests.get")
def test_get_asset_success(mock_get):
    mock_get.return_value = MockResponse({"name": "test_asset"}, 200)

    result = get_asset("123", asset_type="datasets", data_format="json")

    assert result["name"] == "test_asset"

    mock_get.assert_called_once()
    args, kwargs = mock_get.call_args
    assert "datasets" in args[0]

@patch("aiod.calls.calls.requests.get")
def test_get_list_pandas(mock_get):
    mock_get.return_value = MockResponse([{"id": 1}], 200)

    result = get_list(asset_type="datasets", data_format="pandas")

    assert hasattr(result, "shape") 


@patch("aiod.calls.calls.requests.get")
def test_get_any_asset_success(mock_get):
    mock_get.return_value = MockResponse({"id": "123"}, 200)

    result = get_any_asset("123", data_format="json")

    assert result["id"] == "123"

@patch("aiod.calls.calls.requests.get")
def test_get_content(mock_get):
    mock_get.return_value = MockResponse({}, 200, content=b"filedata")

    result = get_content(identifier="123", asset_type="datasets")

    assert result == b"filedata"


@patch("aiod.calls.calls.requests.get")
def test_get_any_asset_server_error(mock_get):
    mock_get.return_value = MockResponse({}, 500)

    with pytest.raises(ServerError):
        get_any_asset("123")

@patch("aiod.calls.calls._get_auth_headers")
@patch("aiod.calls.calls.requests.get")
def test_get_any_asset_headers(mock_get, mock_headers):
    mock_headers.return_value = {"Authorization": "test"}
    mock_get.return_value = MockResponse({"id": "123"}, 200)

    get_any_asset("123")

    _, kwargs = mock_get.call_args
    assert "headers" in kwargs

@patch("aiod.calls.calls.requests.get")
def test_get_any_asset_not_found(mock_get):
    mock_get.return_value = MockResponse({}, HTTPStatus.NOT_FOUND)

    with pytest.raises(KeyError):
        get_any_asset("invalid")

@patch("aiod.calls.calls.requests.post")
@patch("aiod.calls.calls.get_token")
def test_post_asset_failure(mock_token, mock_post):
    mock_token.return_value.headers = {"Authorization": "Bearer token"}
    mock_post.return_value = MockResponse({}, 400)

    result = post_asset(asset_type="datasets", metadata={"name": "test"})

    assert result.status_code == 400


@patch("aiod.calls.calls.requests.get")
def test_get_asset_not_found(mock_get):
    mock_get.return_value = MockResponse(
        {"detail": "not found"}, HTTPStatus.NOT_FOUND
    )

    with pytest.raises(KeyError):
        get_asset("invalid", asset_type="datasets")


@patch("aiod.calls.calls.requests.post")
@patch("aiod.calls.calls.get_token")
def test_post_asset_success(mock_token, mock_post):
    mock_token.return_value.headers = {"Authorization": "Bearer token"}
    mock_post.return_value = MockResponse({"identifier": "abc"}, 200)

    result = post_asset(asset_type="datasets", metadata={"name": "test"})

    assert result == "abc"


@patch("aiod.calls.calls.requests.get")
def test_get_list_basic(mock_get):
    mock_get.return_value = MockResponse([{"id": 1}, {"id": 2}], 200)

    result = get_list(asset_type="datasets", data_format="json")

    assert isinstance(result, list)
    assert len(result) == 2


@patch("aiod.calls.calls.requests.get")
def test_get_list_with_platform(mock_get):
    mock_get.return_value = MockResponse([{"id": 1}], 200)

    result = get_list(
        asset_type="datasets",
        platform="huggingface",
        data_format="json",
    )

    assert result[0]["id"] == 1


@patch("aiod.calls.calls.requests.get")
def test_counts_basic(mock_get):
    mock_get.return_value = MockResponse(10, 200)

    result = counts(asset_type="datasets")

    assert result == 10


@patch("aiod.calls.calls.requests.get")
def test_counts_per_platform(mock_get):
    mock_get.return_value = MockResponse({"hf": 5, "openml": 3}, 200)

    result = counts(asset_type="datasets", per_platform=True)

    assert isinstance(result, dict)
    assert result["hf"] == 5


@patch("aiod.calls.calls.requests.delete")
@patch("aiod.calls.calls.get_token")
def test_delete_asset_success(mock_token, mock_delete):
    mock_token.return_value.headers = {"Authorization": "Bearer token"}
    mock_delete.return_value = MockResponse({}, 200)

    result = delete_asset(asset_type="datasets", identifier="123")

    assert result.status_code == 200


@patch("aiod.calls.calls.requests.delete")
@patch("aiod.calls.calls.get_token")
def test_delete_asset_not_found(mock_token, mock_delete):
    mock_token.return_value.headers = {"Authorization": "Bearer token"}
    mock_delete.return_value = MockResponse(
        {"detail": "not found"}, HTTPStatus.NOT_FOUND
    )

    with pytest.raises(KeyError):
        delete_asset(asset_type="datasets", identifier="invalid")


@patch("aiod.calls.calls.requests.put")
@patch("aiod.calls.calls.get_token")
def test_put_asset_success(mock_token, mock_put):
    mock_token.return_value.headers = {"Authorization": "Bearer token"}
    mock_put.return_value = MockResponse({}, 200)

    res = put_asset(asset_type="datasets", identifier="123", metadata={"name": "test"})

    assert res.status_code == 200


@patch("aiod.calls.calls.requests.put")
@patch("aiod.calls.calls.get_token")
def test_put_asset_not_found(mock_token, mock_put):
    mock_token.return_value.headers = {"Authorization": "Bearer token"}
    mock_put.return_value = MockResponse({"detail": "not found"}, HTTPStatus.NOT_FOUND)

    with pytest.raises(KeyError):
        put_asset(asset_type="datasets", identifier="invalid", metadata={})


@patch("aiod.calls.calls.requests.put")
@patch("aiod.calls.calls.get_token")
@patch("aiod.calls.calls.get_asset")
def test_patch_asset_success(mock_get_asset, mock_token, mock_put):
    mock_get_asset.return_value = {"aiod_entry": "x", "name": "old"}
    mock_token.return_value.headers = {"Authorization": "Bearer token"}
    mock_put.return_value = MockResponse({}, 200)

    res = patch_asset(
        asset_type="datasets",
        identifier="123",
        metadata={"name": "new"}
    )

    assert res.status_code == 200

@patch("aiod.calls.calls.requests.get")
def test_get_asset_from_platform_success(mock_get):
    mock_get.return_value = MockResponse({"id": "123"}, 200)

    res = get_asset_from_platform(
        platform="hf",
        platform_identifier="abc",
        asset_type="datasets",
        data_format="json"
    )

    assert res["id"] == "123"


@patch("aiod.calls.calls.requests.get")
def test_get_asset_from_platform_not_found(mock_get):
    mock_get.return_value = MockResponse(
        {"detail": "not found"}, HTTPStatus.NOT_FOUND
    )

    with pytest.raises(KeyError):
        get_asset_from_platform(
            platform="hf",
            platform_identifier="bad",
            asset_type="datasets"
        )

@patch("aiod.calls.calls.requests.get")
def test_search_success(mock_get):
    mock_get.return_value = MockResponse(
        {"resources": [{"id": 1}]}, 200
    )

    res = search(
        "test",
        asset_type="datasets",
        data_format="json"
    )

    assert isinstance(res, list)
    assert res[0]["id"] == 1

@pytest.mark.asyncio
@patch("aiod.calls.calls._fetch_resources")
async def test_get_assets_async(mock_fetch):
    mock_fetch.return_value = [{"id": 1}, {"id": 2}]

    res = await get_assets_async(
        identifiers=["1", "2"],
        asset_type="datasets",
        data_format="json"
    )

    assert isinstance(res, list)
    assert len(res) == 2

@pytest.mark.asyncio
@patch("aiod.calls.calls._fetch_resources")
async def test_get_list_async(mock_fetch):
    mock_fetch.return_value = [[{"id": 1}], [{"id": 2}]]

    res = await get_list_async(
        asset_type="datasets",
        limit=2,
        batch_size=1,
        data_format="json"
    )

    assert len(res) == 2

def test_get_list_async_invalid_batch():
    import asyncio

    async def run():
        with pytest.raises(ValueError):
            await get_list_async(
                asset_type="datasets",
                batch_size=0
            )

    asyncio.run(run())

@patch("aiod.calls.calls.requests.put")
@patch("aiod.calls.calls.get_token")
@patch("aiod.calls.calls.get_asset")
def test_patch_asset_missing_aiod_entry(mock_get_asset, mock_token, mock_put):
    mock_get_asset.return_value = {"name": "old"} 
    mock_token.return_value.headers = {"Authorization": "Bearer token"}
    mock_put.return_value = MockResponse({}, 200)

    with pytest.raises(KeyError):
        patch_asset(
            asset_type="datasets",
            identifier="123",
            metadata={"name": "new"}
        )