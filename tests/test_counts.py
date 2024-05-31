import responses
from pathlib import Path

import aiod
from aiod.configuration import config


resources_path = Path(__file__).parent / "resources"


def test_counts():
    with responses.RequestsMock() as mocked_requests:
        with open(resources_path / "counts.json", "r") as f:
            res_body = f.read()
        mocked_requests.add(
            responses.GET,
            url=f"{config.api_base_url}counts/{config.version}",
            body=res_body,
            status=200,
        )
        counts = aiod.counts(data_format="json")

        assert isinstance(counts, dict)
        assert "datasets" in counts
