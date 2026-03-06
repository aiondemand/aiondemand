import pytest
import responses
from aioresponses import aioresponses
import asyncio
from aiod.calls import calls
from aiod.configuration import config
from aiod.calls.urls import server_url

@pytest.fixture
def mock_config():
    original_total = config.retry_total
    original_backoff = config.retry_backoff_factor
    config.retry_total = 2
    config.retry_backoff_factor = 0.01  # Fast retries for testing
    yield
    config.retry_total = original_total
    config.retry_backoff_factor = original_backoff

@responses.activate
def test_sync_retry_success_after_failure(mock_config):
    url = server_url() + "assets/1"
    
    # Fail twice, then succeed
    responses.add(responses.GET, url, status=500)
    responses.add(responses.GET, url, status=502)
    responses.add(responses.GET, url, status=200, json={"resource": "success"})

    # This calls get_any_asset -> get_requests_session().get()
    # verify=False to avoid SSL issues in tests if any (though responses mocks it)
    result = calls.get_any_asset("1", data_format="json")
    
    assert result == {"resource": "success"}
    assert len(responses.calls) == 3

@responses.activate
def test_sync_retry_exhaustion(mock_config):
    url = server_url() + "assets/1"
    
    # Fail 3 times (more than retry_total of 2)
    responses.add(responses.GET, url, status=500)
    responses.add(responses.GET, url, status=500)
    responses.add(responses.GET, url, status=500)

    with pytest.raises(Exception): # requests.exceptions.RetryError or similar wrapped error
         calls.get_any_asset("1", data_format="json")

    # Should have tried 1 initial + 2 retries = 3 calls
    assert len(responses.calls) == 3

def test_async_retry_success_after_failure(mock_config):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    url = server_url() + "assets/1"
    
    with aioresponses() as mocked:
        mocked.get(url, status=500)
        mocked.get(url, status=502)
        mocked.get(url, payload={"resource": "success"}, status=200)
        
        # get_assets_async calls _fetch_resources -> robust_request
        result = loop.run_until_complete(
            calls.get_assets_async(identifiers=["1"], asset_type="assets", data_format="json")
        )
        
        assert result == [{"resource": "success"}]
        # aioresponses doesn't easily expose call count in the same way, but we can check if it matched
        # Logic: if it didn't retry, it would have failed at first 500

def test_async_retry_exhaustion(mock_config):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    url = server_url() + "assets/1"
    
    with aioresponses() as mocked:
        mocked.get(url, status=500)
        mocked.get(url, status=500)
        mocked.get(url, status=500)
        
        # Should return the last error response (or raise if we changed robust_request to raise)
        # In robust_request implementation:
        # if attempt < config.retry_total: ... else: return await response.json()
        # So it returns the json of the last error response?
        # Wait, if status is 500, response.json() might fail if body is not json.
        # Let's mock with json body.
        
        # Actually my robust_request implementation returns response.json() on failure.
        # If the server returns 500 with some body, it returns that.
        
        # But `calls.get_assets_async` calls `_fetch_resources`.
        # `_fetch_resources` returns a dict (result of gather).
        # `format_response` might fail if it expects a certain structure.
        
        # Let's adjust expectation. If it returns 500, likely `format_response` or `get_assets_async` flow handles it or raises.
        # `calls.py`: `resources = format_response(response_data, data_format)`
        # If response_data is `[{... error ...}]`, format_response just wraps it.
        
        # For this test, let's verify it returns the 500 content.
        
        # Adding json payload to error responses
        mocked.get(url, status=500, payload={"error": "fail"})
        mocked.get(url, status=500, payload={"error": "fail"})
        mocked.get(url, status=500, payload={"error": "fail"})
        
        result = loop.run_until_complete(
            calls.get_assets_async(identifiers=["1"], asset_type="assets", data_format="json")
        )
        
        # It should return the list of results.
        assert result == [{"error": "fail"}]

