import pytest
import responses

from unittest.mock import Mock, patch
import requests
import jwt

import aiod
from aiod.configuration import config
from aiod.authentication import authentication
from aiod.authentication.authentication import (
    keycloak_openid,
    FailedAuthenticationError,
    login_device_flow,
)


@pytest.fixture
def mocked_token() -> Mock:
    token = {"access_token": "fake_token", "refresh_token": "fake_refresh_token"}
    return Mock(return_value=token)


@pytest.fixture
def mocked_logout() -> Mock:
    return Mock()


def test_authentication(mocked_token: Mock, mocked_logout: Mock):
    keycloak_openid().token = mocked_token
    keycloak_openid().logout = mocked_logout

    access_token = config.access_token
    refresh_token = config.refresh_token
    assert access_token is None, access_token
    assert refresh_token is None, refresh_token

    aiod.login("fake_username", "fake_p455w0rd")
    access_token = config.access_token
    refresh_token = config.refresh_token
    assert access_token == "fake_token", access_token
    assert refresh_token == "fake_refresh_token", refresh_token

    aiod.logout()
    access_token = config.access_token
    refresh_token = config.refresh_token
    assert access_token is None, access_token
    assert refresh_token is None, refresh_token


def test_get_user_endpoint(mocked_token: Mock):
    keycloak_openid().token = mocked_token

    with responses.RequestsMock() as mocked_requests:
        mocked_requests.add(
            responses.GET,
            f"{config.api_base_url}authorization_test",
            json={"name": "user", "roles": ["a_role"]},
            status=200,
        )
        aiod.login("fake_username", "fakeP455w0rd")
        user = aiod.get_current_user()

        header = mocked_requests.calls[0].request.headers["Authorization"]
        assert header == "Bearer fake_token", header
        assert user.name == "user", user
        assert user.roles == ("a_role",), user


def test_device_flow_success(monkeypatch):
    kc = keycloak_openid()
    kc.device = Mock(
        return_value={
            "device_code": "dev123",
            "user_code": "user123",
            "verification_uri": "http://verify",
            "verification_uri_complete": "http://verify?user=user123",
            "interval": 1,
        }
    )
    kc.well_known = Mock(
        return_value={"token_endpoint": "http://token", "jwks_uri": "http://jwks"}
    )

    success_response = Mock()
    success_response.status_code = 200
    success_response.json.return_value = {
        "access_token": "new_token",
        "refresh_token": "new_refresh",
    }
    monkeypatch.setattr(requests, "post", lambda *a, **kw: success_response)

    # Mock JWT validation
    monkeypatch.setattr(
        authentication, "_validate_token", lambda token, jwks: {"sub": "123"}
    )

    login_device_flow(poll_interval=0)  # no sleep
    assert config.access_token == "new_token"
    assert config.refresh_token == "new_refresh"


def test_device_flow_authorization_pending(monkeypatch):
    kc = keycloak_openid()
    kc.device = Mock(
        return_value={
            "device_code": "dev123",
            "user_code": "user123",
            "verification_uri": "http://verify",
            "verification_uri_complete": "http://verify?user=user123",
            "interval": 1,
        }
    )
    kc.well_known = Mock(
        return_value={"token_endpoint": "http://token", "jwks_uri": "http://jwks"}
    )

    # first response pending, second response success
    pending_response = Mock()
    pending_response.status_code = 400
    pending_response.json.return_value = {"error": "authorization_pending"}

    success_response = Mock()
    success_response.status_code = 200
    success_response.json.return_value = {
        "access_token": "token_ok",
        "refresh_token": "refresh_ok",
    }

    calls = iter([pending_response, success_response])
    monkeypatch.setattr(requests, "post", lambda *a, **kw: next(calls))

    monkeypatch.setattr(
        authentication, "_validate_token", lambda token, jwks: {"sub": "123"}
    )

    login_device_flow(poll_interval=0)
    assert config.access_token == "token_ok"
    assert config.refresh_token == "refresh_ok"


def test_device_flow_failure(monkeypatch):
    kc = keycloak_openid()
    kc.device = Mock(
        return_value={
            "device_code": "dev123",
            "user_code": "user123",
            "verification_uri": "http://verify",
            "verification_uri_complete": "http://verify?user=user123",
            "interval": 1,
        }
    )
    kc.well_known = Mock(
        return_value={"token_endpoint": "http://token", "jwks_uri": "http://jwks"}
    )

    error_response = Mock()
    error_response.status_code = 400
    error_response.json.return_value = {"error": "expired_token"}
    monkeypatch.setattr(requests, "post", lambda *a, **kw: error_response)

    with pytest.raises(FailedAuthenticationError):
        login_device_flow(poll_interval=0)
