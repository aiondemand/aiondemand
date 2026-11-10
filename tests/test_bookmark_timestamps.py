"""Regression tests for UTC offsets in bookmark creation timestamps."""

from datetime import timezone

import pytest
import responses

from aiod import bookmarks
from aiod.calls.urls import server_url

# Regression for https://github.com/aiondemand/aiondemand/issues/270.
TIMESTAMPS = [
    pytest.param(
        "2025-09-23T13:01:14",
        "2025-09-23T13:01:14+00:00",
        id="naive-utc",
    ),
    pytest.param(
        "2025-09-23T13:01:14+00:00",
        "2025-09-23T13:01:14+00:00",
        id="explicit-utc",
    ),
    pytest.param(
        "2025-09-23T13:01:14+05:30",
        "2025-09-23T07:31:14+00:00",
        id="positive-offset",
    ),
    pytest.param(
        "2025-09-23T13:01:14-04:00",
        "2025-09-23T17:01:14+00:00",
        id="negative-offset",
    ),
    pytest.param(
        "2025-09-23T13:01:14-03:30",
        "2025-09-23T16:31:14+00:00",
        id="negative-half-hour-offset",
    ),
    pytest.param(
        "2025-09-23T13:01:14.123456+05:30",
        "2025-09-23T07:31:14.123456+00:00",
        id="fractional-seconds",
    ),
    pytest.param(
        "2025-01-01T00:15:00+05:45",
        "2024-12-31T18:30:00+00:00",
        id="previous-year",
    ),
    pytest.param(
        "2025-12-31T23:45:00-04:00",
        "2026-01-01T03:45:00+00:00",
        id="next-year",
    ),
]


@pytest.mark.parametrize("timestamp,expected", TIMESTAMPS)
@responses.activate
def test_register_bookmark_timestamp(valid_refresh_token, timestamp, expected):
    """Normalize creation responses to UTC without changing their instant."""
    responses.post(
        f"{server_url()}bookmarks",
        json={"resource_identifier": "data_example", "created_at": timestamp},
    )

    bookmark = bookmarks.register("data_example")

    assert bookmark.identifier == "data_example"
    assert bookmark.created.isoformat() == expected
    assert bookmark.created.tzinfo is timezone.utc


@pytest.mark.parametrize("timestamp,expected", TIMESTAMPS)
@responses.activate
def test_list_bookmark_timestamp(valid_refresh_token, timestamp, expected):
    """Normalize listed bookmarks using the same UTC rules as registration."""
    responses.get(
        f"{server_url()}bookmarks",
        json=[{"resource_identifier": "data_example", "created_at": timestamp}],
    )

    result = bookmarks.get_list()

    assert len(result) == 1
    assert result[0].identifier == "data_example"
    assert result[0].created.isoformat() == expected
    assert result[0].created.tzinfo is timezone.utc
