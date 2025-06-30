""" Tests which connect to the server.

Do not add new tests unless there is a very good reason.
These tests do not run with the default test configuration.

"""
import pytest

import aiod


@pytest.mark.server()
def test_get_dataset_from_server():
    datasets = aiod.datasets.get_list()
    assert len(datasets) == 10
    dataset = aiod.datasets.get_asset(datasets["identifier"].iloc[0])
    assert dataset["name"] == datasets["name"].iloc[0]
