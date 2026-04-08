"""Utility functions for testing."""

import logging

import requests

logger = logging.getLogger(__name__)


def is_aiod_server_available(timeout: int = 5) -> bool:
    """Check if the AIoD API server is available.

    Parameters
    ----------
    timeout : int, default=5
        Timeout in seconds for the health check request.

    Returns
    -------
    bool
        True if the server is reachable and responding, False otherwise.

    """
    from aiod.configuration import config

    try:
        # Try to reach the API server root endpoint
        response = requests.get(
            config.api_server,
            timeout=timeout,
            allow_redirects=True,
        )
        # Consider 2xx and 3xx status codes as "available"
        is_available = response.status_code < 400
        if is_available:
            logger.info(f"AIoD server is available at {config.api_server}")
        else:
            logger.warning(
                f"AIoD server returned status {response.status_code} "
                f"at {config.api_server}"
            )
        return is_available
    except requests.exceptions.RequestException as e:
        logger.warning(f"AIoD server is not available: {e}")
        return False


def skip_if_server_unavailable():
    """Pytest decorator to skip tests if the AIoD server is not available.

    Examples
    --------
    >>> import pytest
    >>> from tests.utils import skip_if_server_unavailable
    >>>
    >>> @pytest.mark.server()
    >>> @skip_if_server_unavailable()
    >>> def test_something_with_server():
    ...     # This test will be skipped if server is down
    ...     pass

    """
    import pytest

    return pytest.mark.skipif(
        not is_aiod_server_available(),
        reason="AIoD server is not available",
    )
