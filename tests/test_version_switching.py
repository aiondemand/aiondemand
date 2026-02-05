"""Tests for API version switching functionality."""

import pytest
import responses

from aiod import config, use_version, datasets
from aiod.calls.urls import server_url


class TestVersionSwitching:
    """Test the use_version context manager for switching API versions."""

    def test_use_version_context_manager(self):
        """Test that use_version temporarily changes the API version."""
        original_version = config.version
        assert original_version == "not_set"  # From conftest setup

        # Version should change inside context
        with use_version("v1"):
            assert config.version == "v1"

        # Version should be restored after context
        assert config.version == original_version

    def test_use_version_nested(self):
        """Test that use_version works with nested contexts."""
        original_version = config.version

        with use_version("v1"):
            assert config.version == "v1"

            with use_version("v2"):
                assert config.version == "v2"

            # Should restore to v1
            assert config.version == "v1"

        # Should restore to original
        assert config.version == original_version

    def test_use_version_with_exception(self):
        """Test that use_version restores version even when exception occurs."""
        original_version = config.version

        with pytest.raises(ValueError):
            with use_version("v3"):
                assert config.version == "v3"
                raise ValueError("Test exception")

        # Version should still be restored
        assert config.version == original_version

    def test_server_url_with_version(self):
        """Test that server_url correctly uses the configured version."""
        config.version = "v2"
        assert server_url() == "http://not.set/v2/"

        with use_version("v1"):
            assert server_url() == "http://not.set/v1/"

        assert server_url() == "http://not.set/v2/"

    def test_server_url_with_empty_version(self):
        """Test that server_url works with empty version string."""
        with use_version(""):
            assert server_url() == "http://not.set/"

    def test_server_url_with_latest(self):
        """Test using 'latest' as version."""
        with use_version("latest"):
            assert server_url() == "http://not.set/latest/"

    @responses.activate
    def test_api_calls_use_correct_version(self):
        """Test that API calls use the correct version from context manager."""
        # Mock v1 endpoint
        responses.add(
            responses.GET,
            "http://not.set/v1/datasets?offset=0&limit=5",
            json=[{"identifier": "data_v1_test", "name": "Test Dataset V1"}],
            status=200,
        )

        # Mock v2 endpoint
        responses.add(
            responses.GET,
            "http://not.set/v2/datasets?offset=0&limit=5",
            json=[{"identifier": "data_v2_test", "name": "Test Dataset V2"}],
            status=200,
        )

        # Default version (v2 from config, but we set to not_set in tests)
        config.version = "v2"
        result_v2 = datasets.get_list(limit=5, data_format="json")
        assert result_v2[0]["identifier"] == "data_v2_test"

        # Use v1 version
        with use_version("v1"):
            result_v1 = datasets.get_list(limit=5, data_format="json")
            assert result_v1[0]["identifier"] == "data_v1_test"

        # Back to v2
        result_v2_again = datasets.get_list(limit=5, data_format="json")
        assert result_v2_again[0]["identifier"] == "data_v2_test"

    def test_version_override_parameter_takes_precedence(self):
        """Test that explicit version parameter overrides context manager."""
        config.version = "v2"

        with use_version("v1"):
            # Explicit version parameter should override context manager
            url = server_url(version="v3")
            assert url == "http://not.set/v3/"

    def test_permanent_version_change(self):
        """Test permanently changing the version via config."""
        original_version = config.version

        # Permanent change
        config.version = "v1"
        assert config.version == "v1"
        assert server_url() == "http://not.set/v1/"

        # Restore
        config.version = original_version
