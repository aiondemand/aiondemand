from aiod.calls.urls import url_to_get_list
from aiod.configuration import config


def test_server_without_trailing_slash() -> None:
    old_api_server = config.api_server
    old_version = config.version
    try:
        config.api_server = "http://localhost:8000"
        config.version = "v2"
        url = url_to_get_list("datasets")
        assert url == "http://localhost:8000/v2/datasets?offset=0&limit=10"
    finally:
        config.api_server = old_api_server
        config.version = old_version


def test_server_with_trailing_slash() -> None:
    old_api_server = config.api_server
    old_version = config.version
    try:
        config.api_server = "http://localhost:8000/"
        config.version = "v2"
        url = url_to_get_list("datasets")
        assert url == "http://localhost:8000/v2/datasets?offset=0&limit=10"
    finally:
        config.api_server = old_api_server
        config.version = old_version
