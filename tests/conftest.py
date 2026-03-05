import json
import re
from http import HTTPStatus

import pytest
import requests
import responses

from aiod import config
import aiod.authentication.authentication as authentication

# Cache the server reachability check so it runs only once per test session.
_server_reachable = None
_server_skip_reason = ""


@pytest.fixture(autouse=True)
def skip_if_server_unreachable(request):
    """Auto-skip @pytest.mark.server tests when the AIoD API is unreachable."""
    if not request.node.get_closest_marker("server"):
        return

    global _server_reachable, _server_skip_reason
    if _server_reachable is None:
        try:
            response = requests.get(config.api_server, timeout=300)
            response.raise_for_status()
            _server_reachable = True
        except (requests.ConnectionError, requests.Timeout) as e:
            _server_reachable = False
            _server_skip_reason = (
                "AIoD server unreachable. "
                f"{type(e).__name__}: {e}"
            )

    if not _server_reachable:
        pytest.skip(_server_skip_reason)


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
def mocked_keycloak_server():
    url = "http://not.set/realms/not_set/protocol/openid-connect/token"

    def validate_refresh_token(request):
        match = re.match(
            r"client_id=(\w+)&grant_type=(\w+)&refresh_token=(\w+)", request.body
        )
        assert match, "Request type not yet added to mock."
        client, grant_type, token = match.groups()
        match (client, grant_type, token):
            case _, "refresh_token", "invalid":
                error = {
                    "error": "invalid_grant",
                    "error_description": "Invalid refresh token",
                }
                return HTTPStatus.BAD_REQUEST, {}, json.dumps(error)
            case _, "refresh_token", "expired":
                error = {
                    "error": "invalid_grant",
                    "error_description": "Offline user session not found",
                }
                return HTTPStatus.BAD_REQUEST, {}, json.dumps(error)
            case _, "refresh_token", "valid":
                body = {
                    "access_token": "valid_access",
                    "refresh_token": "valid",
                    "expires_in": 30,
                }
                return HTTPStatus.OK, {}, json.dumps(body)
            case unknown:
                raise RuntimeError(f"Unknown request payload: {unknown}")

    responses.add_callback(
        responses.POST,
        url,
        callback=validate_refresh_token,
    )
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
