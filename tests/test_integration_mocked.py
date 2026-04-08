"""Mock-based integration tests that don't depend on live server.

These tests provide the same coverage as server-based integration tests
but use mocked responses instead of connecting to the live AIoD server.
"""

import pytest
import responses

import aiod


@pytest.fixture(autouse=True)
def setup_config():
    """Ensure config is properly set for tests."""
    # Store original values
    original_api_server = aiod.config.api_server
    original_version = aiod.config.version
    
    # Set test configuration
    aiod.config.api_server = "https://api.aiod.eu/"
    aiod.config.version = "v2"
    
    yield
    
    # Restore original values
    aiod.config.api_server = original_api_server
    aiod.config.version = original_version


@responses.activate
def test_get_dataset_list_mocked():
    """Test getting dataset list with mocked API response."""
    # Mock the API response - the API returns results in a list
    mock_results = [
        {
            "identifier": i,
            "name": f"Test Dataset {i}",
            "platform": "test_platform",
            "platform_resource_identifier": f"test_id_{i}",
            "date_published": "2024-01-01",
            "same_as": f"https://example.com/dataset{i}",
            "is_accessible_for_free": True,
        }
        for i in range(1, 11)
    ]

    responses.add(
        responses.GET,
        "https://api.aiod.eu/v2/datasets?offset=0&limit=10",
        json=mock_results,
        status=200,
    )

    # Test the function
    datasets = aiod.datasets.get_list()
    assert len(datasets) == 10
    assert datasets["name"].iloc[0] == "Test Dataset 1"


@responses.activate
def test_get_dataset_asset_mocked():
    """Test getting a specific dataset asset with mocked API response."""
    dataset_id = 1
    mock_dataset = {
        "identifier": dataset_id,
        "name": "Test Dataset 1",
        "platform": "test_platform",
        "platform_resource_identifier": "test_id_1",
        "date_published": "2024-01-01",
        "same_as": "https://example.com/dataset1",
        "is_accessible_for_free": True,
        "description": "A test dataset",
    }

    responses.add(
        responses.GET,
        f"https://api.aiod.eu/v2/datasets/{dataset_id}",
        json=mock_dataset,
        status=200,
    )

    # Test the function
    dataset = aiod.datasets.get_asset(dataset_id)
    assert dataset["name"] == "Test Dataset 1"
    assert dataset["identifier"] == dataset_id


@responses.activate
@pytest.mark.parametrize("version", ["v2", ""])
def test_get_dataset_list_different_versions_mocked(version: str):
    """Test getting dataset list with different API versions."""
    # Set the version
    aiod.config.version = version

    # Construct the URL based on version
    if version:
        url = f"https://api.aiod.eu/{version}/datasets?offset=0&limit=10"
    else:
        url = "https://api.aiod.eu/datasets?offset=0&limit=10"

    mock_results = [
        {
            "identifier": i,
            "name": f"Dataset {i}",
            "platform": "test",
        }
        for i in range(1, 11)
    ]

    responses.add(
        responses.GET,
        url,
        json=mock_results,
        status=200,
    )

    # Test the function
    datasets = aiod.datasets.get_list()
    assert len(datasets) == 10
