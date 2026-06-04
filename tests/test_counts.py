import json
from pathlib import Path

import aiod
from aiod.calls.urls import server_url
from aiod.configuration import config

resources_path = Path(__file__).parent / "resources"


def test_counts(httpx_mock):
    with open(resources_path / "counts.json") as f:
        res_body = json.load(f)
    config.version = "v1"
    httpx_mock.add_response(
        method="GET",
        url=f"{server_url()}counts",
        json=res_body,
    )
    counts = aiod.counts(data_format="json")

    assert isinstance(counts, dict)
    assert "datasets" in counts
