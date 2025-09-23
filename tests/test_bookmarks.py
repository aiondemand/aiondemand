import pytest
import responses
from responses import matchers

import aiod.bookmarks


@responses.activate
def test_create_bookmark(valid_refresh_token):
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
def test_create_bookmark_invalid_identifier(valid_refresh_token):
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