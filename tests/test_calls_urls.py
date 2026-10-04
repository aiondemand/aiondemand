from unittest.mock import patch

from aiod.calls import urls
from aiod.configuration import config


def test_server_url_default():
    # Assuming config.version and config.api_server are defaults
    with patch.object(config, 'api_server', 'https://api.aiodp.eu/'):
        with patch.object(config, 'version', 'v2'):
            assert urls.server_url() == "https://api.aiodp.eu/v2/"
            assert urls.server_url(version="v1") == "https://api.aiodp.eu/v1/"
            assert urls.server_url(version="") == "https://api.aiodp.eu/"


def test_url_to_get_asset():
    with patch.object(config, 'api_server', 'https://test/'):
        with patch.object(config, 'version', 'v1'):
            url = urls.url_to_get_asset("datasets", "123")
            assert url == "https://test/v1/datasets/123"


def test_url_to_get_list():
    with patch.object(config, 'api_server', 'https://test/'):
        with patch.object(config, 'version', 'v1'):
            url = urls.url_to_get_list("datasets", offset=10, limit=20)
            assert url == "https://test/v1/datasets?offset=10&limit=20"


def test_url_to_search():
    with patch.object(config, 'api_server', 'https://test/'):
        with patch.object(config, 'version', 'v1'):
            url = urls.url_to_search(
                asset_type="datasets",
                search_query="machine learning",
                platforms=["zenodo", "aiod"],
                offset=0,
                limit=10,
                search_fields="name",
                get_all=True
            )
            # doseq=True spreads platforms.
            # "machine learning" should be quoted to "machine+learning"
            assert "search/datasets?" in url
            assert "search_query=machine+learning" in url
            assert "platforms=zenodo&platforms=aiod" in url
            assert "search_fields=name" in url
            assert "get_all=true" in url


def test_url_to_resource_counts():
    with patch.object(config, 'api_server', 'https://test/'):
        with patch.object(config, 'version', 'v1'):
            url = urls.url_to_resource_counts(
                per_platform=True, asset_type="datasets"
            )
            assert url == "https://test/v1/counts/datasets?detailed=true"


def test_url_to_get_content():
    with patch.object(config, 'api_server', 'https://test/'):
        with patch.object(config, 'version', 'v1'):
            url = urls.url_to_get_content("datasets", "123", distribution_idx=2)
            assert url == "https://test/v1/datasets/123/content/2"

            url_no_idx = urls.url_to_get_content("datasets", "123", distribution_idx=0)
            assert url_no_idx == "https://test/v1/datasets/123/content"


def test_url_to_get_list_from_platform():
    with patch.object(config, 'api_server', 'https://test/'):
        with patch.object(config, 'version', 'v1'):
            url = urls.url_to_get_list_from_platform(
                "datasets", "zenodo", offset=5, limit=5
            )
            assert url == "https://test/v1/platforms/zenodo/datasets?offset=5&limit=5"


def test_url_to_get_asset_from_platform():
    with patch.object(config, 'api_server', 'https://test/'):
        with patch.object(config, 'version', 'v1'):
            url = urls.url_to_get_asset_from_platform(
                "datasets", "zenodo", "zenodo.123"
            )
            assert url == "https://test/v1/platforms/zenodo/datasets/zenodo.123"
