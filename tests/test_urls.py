import pytest

from aiod.calls.urls import url_to_get_list
from aiod.configuration import config


@pytest.mark.parametrize(
    "api_server",
    [
        "http://localhost:8000",
        "http://localhost:8000/",
    ],
)
def test_server_url_normalization(api_server: str) -> None:
    old_api_server = config.api_server
    old_version = config.version
    try:
        config.api_server = api_server
        config.version = "v2"
        url = url_to_get_list("datasets")
        assert url == "http://localhost:8000/v2/datasets?offset=0&limit=10"
    finally:
        config.api_server = old_api_server
        config.version = old_version
