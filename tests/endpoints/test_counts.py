import responses
from pathlib import Path

import aiod_sdk as aiod
from aiod_sdk.endpoints.endpoint import API_BASE_URL, LATEST_VERSION

resources_path = Path(__file__).parent.parent / "resources"


def test_counts():
    with responses.RequestsMock() as mocked_requests:
        with open(resources_path / "counts.json", "r") as f:
            res_body = f.read()
        mocked_requests.add(
            responses.GET,
            API_BASE_URL + "counts/" + LATEST_VERSION,
            body=res_body,
            status=200,
        )
        res = aiod.counts()

        assert res.status_code == 200
        assert "datasets" in res.json()
