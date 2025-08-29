import pytest

from aiod import config
import aiod.authentication.authentication as authentication


@pytest.fixture(autouse=True)
def setup_test_configuration():
    # User defaults are autoloaded, so we override them.
    config.auth_server = "http://not.set"
    config.api_server = "http://not.set"
    config.realm = "not_set"
    config.version = "not_set"
    config.client_id = "not_set"


@pytest.fixture(autouse=True)
def setup_test_authentication():
    # User token is autoloaded, so we override it.
    authentication._token = None
