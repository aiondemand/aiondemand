"""Integration tests for the AIoD SDK.

Live server tests (marked ``@pytest.mark.server``) are skipped automatically
when the AIoD API is unreachable — see ``conftest.py::skip_if_server_unreachable``.

Mocked integration tests exercise the same SDK workflows against realistic
fixtures so that CI always has integration-level coverage.
"""

import json

import pytest
import responses

import aiod
from aiod.calls.urls import server_url

# ---------------------------------------------------------------------------
# Realistic fixture data (matches the shape returned by the real API)
# ---------------------------------------------------------------------------

_DATASET_LIST_FIXTURE = [
    {
        "identifier": "data_00000000000000000000000001",
        "name": "Example Dataset 1",
        "platform": "aiod",
        "description": {"plain": "First example dataset."},
    },
    {
        "identifier": "data_00000000000000000000000002",
        "name": "Example Dataset 2",
        "platform": "aiod",
        "description": {"plain": "Second example dataset."},
    },
]

_DATASET_DETAIL_FIXTURE = {
    "identifier": "data_00000000000000000000000001",
    "name": "Example Dataset 1",
    "platform": "aiod",
    "description": {"plain": "First example dataset."},
    "same_as": "https://example.org/dataset/1",
}

# ---------------------------------------------------------------------------
# Mocked integration tests — always run in CI (no server dependency)
# ---------------------------------------------------------------------------


@responses.activate
@pytest.mark.parametrize("version", ["default", ""])
def test_get_dataset_list_mocked(version: str):
    """Verify get_list -> get_asset flow with mocked responses."""
    if version == "":
        aiod.config.version = ""
    else:
        aiod.config.version = "not_set"

    base_url = server_url()

    responses.add(
        responses.GET,
        f"{base_url}datasets?offset=0&limit=10",
        json=_DATASET_LIST_FIXTURE,
        status=200,
    )
    datasets = aiod.datasets.get_list()
    assert len(datasets) == 2

    first_id = datasets["identifier"].iloc[0]
    responses.add(
        responses.GET,
        f"{base_url}datasets/{first_id}",
        json=_DATASET_DETAIL_FIXTURE,
        status=200,
    )
    dataset = aiod.datasets.get_asset(first_id, data_format="json")
    assert dataset["name"] == datasets["name"].iloc[0]


# ---------------------------------------------------------------------------
# Live server tests — run only when explicitly requested AND server is up
# ---------------------------------------------------------------------------

DEFAULT_MARKER = "default"
LATEST_VERSION_MARKER = ""


@pytest.mark.server()
@pytest.mark.parametrize("version", [DEFAULT_MARKER, LATEST_VERSION_MARKER])
def test_get_dataset_list_from_default_version_server(version: str):
    if version == LATEST_VERSION_MARKER:
        aiod.config.version = LATEST_VERSION_MARKER
    aiod.config.request_timeout_seconds = 100
    datasets = aiod.datasets.get_list()
    assert len(datasets) == 10
    dataset = aiod.datasets.get_asset(datasets["identifier"].iloc[0])
    assert dataset["name"] == datasets["name"].iloc[0]
