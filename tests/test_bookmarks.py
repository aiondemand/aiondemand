import pytest

import aiod.bookmarks


def test_bookmark_create(valid_refresh_token, httpx_mock):
    httpx_mock.add_response(
        method="POST",
        url="http://not.set/not_set/bookmarks?resource_identifier=valid_identifier",
        match_headers={"Authorization": "Bearer valid_access"},
        json={
            "resource_identifier": "valid_identifier",
            "created_at": "2025-09-23T13:01:14",
        },
    )
    bookmark = aiod.bookmarks.register("valid_identifier")
    assert bookmark.identifier == "valid_identifier"
    assert bookmark.created.isoformat() == "2025-09-23T13:01:14+00:00"


def test_bookmark_create_invalid_identifier(valid_refresh_token, httpx_mock):
    httpx_mock.add_response(
        method="POST",
        url="http://not.set/not_set/bookmarks?resource_identifier=not_an_identifier",
        match_headers={"Authorization": "Bearer valid_access"},
        json={
            "detail": "Resource not_an_identifier does not exist.",
            "reference": "9745791405d945c084865ea2c3e4bc7b",
        },
        status_code=404,
    )
    with pytest.raises(KeyError):
        aiod.bookmarks.register("not_an_identifier")


def test_bookmark_delete(valid_refresh_token, httpx_mock):
    httpx_mock.add_response(
        method="DELETE",
        url="http://not.set/not_set/bookmarks?resource_identifier=valid_identifier",
        match_headers={"Authorization": "Bearer valid_access"},
        status_code=200,
    )
    aiod.bookmarks.delete("valid_identifier")


def test_bookmark_list(valid_refresh_token, httpx_mock):
    httpx_mock.add_response(
        method="GET",
        url="http://not.set/not_set/bookmarks",
        match_headers={"Authorization": "Bearer valid_access"},
        json=[
            {
                "resource_identifier": "data_04BadJ7gCY3CZIR2Y1QDG8Z2",
                "created_at": "2025-09-23T13:01:14",
            },
            {
                "resource_identifier": "mdl_AbFo3gwAWsQ3HxLG90RC2GWH",
                "created_at": "2025-09-22T14:10:09",
            },
        ],
    )
    bookmarks = aiod.bookmarks.get_list()
    assert len(bookmarks) == 2, "Each element should be included in the response"
    assert bookmarks[0].identifier.startswith("data"), "Each element should be parsed to a Bookmark"
