import pytest
import responses

import aiod_sdk as aiod

from aiod_sdk.endpoints.endpoint import Endpoint, API_BASE_URL, LATEST_VERSION


class TestEndpoint(Endpoint):
    name = "test"


endpoint_list = [
    "case_studies",
    "computational_assets",
    "contacts",
    "datasets",
    "educational_resources",
    "events",
    "experiments",
    "ml_models",
    "news",
    "organisations",
    "persons",
    "platforms",
    "projects",
    "publications",
    "services",
    "teams",
]


@pytest.fixture(params=endpoint_list)
def endpoint_name(request):
    return request.param


def test_endpoints_are_created(endpoint_name):

    endpoint = getattr(aiod, endpoint_name)
    assert endpoint.name == endpoint_name
    assert issubclass(endpoint, Endpoint)


def test_endpoint_list(endpoint_name):
    with responses.RequestsMock() as mocked_requests:
        mocked_requests.add(
            responses.GET,
            API_BASE_URL + f"{endpoint_name}/" + LATEST_VERSION + "?offset=0&limit=10",
            body=b'[{"resource_1": "info"},{"resource_2": "info"}]',
            status=200,
        )
        endpoint = getattr(aiod, endpoint_name)
        metadata_list = endpoint.list()

        assert len(metadata_list) == 2


def test_endpoint_counts(endpoint_name):
    with responses.RequestsMock() as mocked_requests:
        mocked_requests.add(
            responses.GET,
            API_BASE_URL
            + "counts/"
            + f"{endpoint_name}/"
            + LATEST_VERSION
            + "?detailed=false",
            body=b"2",
            status=200,
        )
        endpoint = getattr(aiod, endpoint_name)
        counts = endpoint.counts()

        assert counts == 2


def test_endpoint_get(endpoint_name):
    with responses.RequestsMock() as mocked_requests:
        mocked_requests.add(
            responses.GET,
            API_BASE_URL + f"{endpoint_name}/" + LATEST_VERSION + "/" + "1",
            body=b'{"resource":"fake_details"}',
            status=200,
        )
        endpoint = getattr(aiod, endpoint_name)
        metadata = endpoint.get(identifier=1, format="dict")

        assert metadata == {"resource": "fake_details"}
