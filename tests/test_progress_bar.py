import asyncio

from aioresponses import aioresponses

import aiod
from aiod.calls.urls import server_url


def test_get_assets_async_with_progress_bar():
    """Verify that `get_assets_async` does not crash when `show_progress=True`.

    Matches project style: uses manual event loop instead of pytest-asyncio.
    """
    # 1. Setup the Loop manually (Project Style)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    asset_type = "datasets"
    identifier = "1"
    url = f"{server_url()}{asset_type}/{identifier}"

    with aioresponses() as mocked_responses:
        # Mock a successful API response
        mocked_responses.get(url, payload={"name": "Test Dataset"}, status=200)

        # 2. Run the async function until complete
        result = loop.run_until_complete(
            aiod.datasets.get_assets_async(
                identifiers=[identifier],
                show_progress=True,
                data_format="json",
            )
        )

        assert len(result) == 1
        assert result[0]["name"] == "Test Dataset"

    loop.close()


def test_get_list_async_with_progress_bar():
    """Verify that `get_list_async` does not crash when `show_progress=True`."""
    # 1. Setup the Loop manually
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    asset_type = "datasets"
    # Note: calls.py logic adds offset/limit to the URL
    url = f"{server_url()}{asset_type}?limit=1&offset=0"

    with aioresponses() as mocked_responses:
        # Mock a successful API response
        mocked_responses.get(url, payload=[{"name": "Test Dataset 1"}], status=200)

        # 2. Run the async function until complete
        result = loop.run_until_complete(
            aiod.datasets.get_list_async(
                limit=1,
                batch_size=1,
                show_progress=True,
                data_format="json",
            )
        )

        assert len(result) == 1
        assert result[0]["name"] == "Test Dataset 1"

    loop.close()