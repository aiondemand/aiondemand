from unittest.mock import patch

import pytest
from keycloak import KeycloakPostError

import aiod.authentication.authentication as authentication
from aiod import config


@pytest.fixture(autouse=True)
def setup_test_configuration(request):
    if "server" in request.keywords:
        return
    # User defaults are autoloaded, so we override them.
    config.api_server = "http://not.set/"
    config.version = "not_set"
    config.auth_server = "http://not.set/"
    config.realm = "not_set"
    config.client_id = "not_set"


@pytest.fixture(autouse=True)
def mocked_keycloak_server(setup_test_configuration):
    """Mock Token._refresh() at the Python level so no HTTP is needed."""

    def mock_refresh(refresh_token):
        if refresh_token in ("invalid", "expired"):
            raise KeycloakPostError(
                error_message="invalid_grant",
                response_code=400,
                response_body=b'{"error": "invalid_grant"}',
            )
        return {
            "access_token": "valid_access",
            "refresh_token": "valid",
            "expires_in": 30,
        }

    kc = authentication.keycloak_openid()
    with patch.object(kc, "refresh_token", side_effect=mock_refresh):
        yield


@pytest.fixture(autouse=True)
def no_token():
    # User token is autoloaded, so we override it.
    authentication._token = None


@pytest.fixture
def expired_refresh_token():
    authentication._token = authentication.Token(
        refresh_token="expired",
    )


@pytest.fixture
def valid_refresh_token():
    authentication._token = authentication.Token(
        refresh_token="valid",
    )


@pytest.fixture
def invalid_refresh_token():
    authentication._token = authentication.Token(
        refresh_token="invalid",
    )
