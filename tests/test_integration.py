"""Tests which connect to the server.

Do not add new tests unless there is a very good reason.
These tests do not run with the default test configuration.

"""

import pytest

import aiod

DEFAULT_MARKER = "default"
LATEST_VERSION_MARKER = ""


@pytest.mark.server()
@pytest.mark.parametrize("version", [DEFAULT_MARKER, LATEST_VERSION_MARKER])
def test_get_dataset_list_from_default_version_server(version: str):
    if version == LATEST_VERSION_MARKER:
        aiod.config.version = LATEST_VERSION_MARKER
    datasets = aiod.datasets.get_list()
    assert len(datasets) == 10
    dataset = aiod.datasets.get_asset(datasets["identifier"].iloc[0])
    assert dataset["name"] == datasets["name"].iloc[0]
