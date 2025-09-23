import pytest
import responses
from responses import matchers

import aiod.bookmarks


@responses.activate
def test_bookmark_create(valid_refresh_token):
    responses.post(
        "http://not.set/not_set/bookmarks?resource_identifier=valid_identifier",
        json={
            "resource_identifier": "valid_identifier",
            "created_at": "2025-09-23T13:01:14"
        },
        match=[matchers.header_matcher({"Authorization": "Bearer valid_access"})],
    )
    bookmark = aiod.bookmarks.register("valid_identifier")
    assert bookmark.identifier == "valid_identifier"
    assert bookmark.created.isoformat() == "2025-09-23T13:01:14+00:00"


@responses.activate
def test_bookmark_create_invalid_identifier(valid_refresh_token):
    responses.post(
        "http://not.set/not_set/bookmarks?resource_identifier=not_an_identifier",
        json={
            "detail": "Resource not_an_identifier does not exist.",
            "reference": "9745791405d945c084865ea2c3e4bc7b"
        },
        match=[matchers.header_matcher({"Authorization": "Bearer valid_access"})],
    )
    with pytest.raises(KeyError):
        aiod.bookmarks.register("not_an_identifier")


@responses.activate
def test_bookmark_delete(valid_refresh_token):
    responses.delete(
        "http://not.set/not_set/bookmarks?resource_identifier=valid_identifier",
        match=[matchers.header_matcher({"Authorization": "Bearer valid_access"})],
    )
    aiod.bookmarks.delete("valid_identifier")


@responses.activate
def test_bookmark_list(valid_refresh_token):
    responses.get(
        "http://not.set/not_set/bookmarks",
        json=[
          {
            "resource_identifier": "data_04BadJ7gCY3CZIR2Y1QDG8Z2",
            "created_at": "2025-09-23T13:01:14"
          },
          {
            "resource_identifier": "mdl_AbFo3gwAWsQ3HxLG90RC2GWH",
            "created_at": "2025-09-22T14:10:09"
          }
        ],
        match=[matchers.header_matcher({"Authorization": "Bearer valid_access"})],
    )
    bookmarks = aiod.bookmarks.get_list()
    assert len(bookmarks) == 2, "Each element should be included in the response"
    assert bookmarks[0].identifier.startswith("data"), "Each element should be parsed to a Bookmark"
