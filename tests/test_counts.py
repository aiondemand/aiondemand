from pathlib import Path

import responses

import aiod
from aiod.calls.urls import server_url
from aiod.configuration import config

resources_path = Path(__file__).parent / "resources"


def test_counts():
    with responses.RequestsMock() as mocked_requests:
        with open(resources_path / "counts.json") as f:
            res_body = f.read()
        config.version = "v1"
        mocked_requests.add(
            responses.GET,
            url=f"{server_url()}counts",
            body=res_body,
            status=200,
        )
        counts = aiod.counts(data_format="json")

        assert isinstance(counts, dict)
        assert "datasets" in counts
