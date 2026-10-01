"""Tests which connect to an AIoD server.

These tests are deselected by default (see the ``-m 'not server'`` addopts in
``pyproject.toml``), because they need a reachable AIoD server. To run them,
override the marker expression on the command line::

    pytest -m server tests/test_integration.py

Do not add new tests unless there is a very good reason.

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
    aiod.config.request_timeout_seconds = 100
    datasets = aiod.datasets.get_list()
    assert len(datasets) == 10
    dataset = aiod.datasets.get_asset(datasets["identifier"].iloc[0])
    assert dataset["name"] == datasets["name"].iloc[0]
