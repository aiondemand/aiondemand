import responses

import aiod_sdk as aiod

from aiod_sdk.endpoints.endpoint import Endpoint, API_BASE_URL, LATEST_VERSION


class TestEndpoint(Endpoint):
    name = "test"


def test_endpoints_are_created():

    assert aiod.case_studies.name == "case_studies"
    assert issubclass(aiod.case_studies, Endpoint)

    assert aiod.computational_assets.name == "computational_assets"
    assert issubclass(aiod.computational_assets, Endpoint)

    assert aiod.platforms.name == "platforms"
    assert issubclass(aiod.platforms, Endpoint)


def test_endpoint_list():
    with responses.RequestsMock() as mocked_requests:
        mocked_requests.add(
            responses.GET,
            API_BASE_URL + "test/" + LATEST_VERSION + "?offset=0&limit=10",
            body=b'["resource_1","resource_2"]',
            status=200,
        )
        res = TestEndpoint.list()

        assert res.status_code == 200
        assert len(res.json()) == 2


def test_endpoint_counts():
    with responses.RequestsMock() as mocked_requests:
        mocked_requests.add(
            responses.GET,
            API_BASE_URL + "counts/" + "test/" + LATEST_VERSION + "?detailed=false",
            body=b"2",
            status=200,
        )
        res = TestEndpoint.counts()

        assert res.status_code == 200
        assert res.json() == 2


def test_endpoint_get():
    with responses.RequestsMock() as mocked_requests:
        mocked_requests.add(
            responses.GET,
            API_BASE_URL + "test/" + LATEST_VERSION + "/" + "1",
            body=b'{"resource":"fake_details"}',
            status=200,
        )
        res = TestEndpoint.get(identifier=1)

        assert res.status_code == 200
        assert res.json() == {"resource": "fake_details"}
