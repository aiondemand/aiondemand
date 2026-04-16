import logging

import pytest
import responses
from responses import matchers

from unittest.mock import Mock, patch
import requests

import aiod
from aiod.configuration import config
from aiod.authentication import authentication
from aiod.authentication.authentication import (
    keycloak_openid,
    AuthenticationError,
    create_token,
    get_token,
    set_token,
    Token,
    NotAuthenticatedError,
)


@pytest.fixture
def mocked_token() -> Mock:
    token = {"access_token": "fake_token", "refresh_token": "fake_refresh_token"}
    return Mock(return_value=token)


@pytest.fixture
def mocked_logout() -> Mock:
    return Mock()


def test_get_user_endpoint(mocked_token: Mock):
    keycloak_openid().token = mocked_token

    with responses.RequestsMock() as mocked_requests:
        mocked_requests.add(
            responses.GET,
            f"{config.api_server}authorization_test",
            json={"name": "user", "roles": ["a_role"]},
            status=200,
        )
        set_token(
            Token(refresh_token="fake_refresh", access_token="fake_token", expires_in_seconds=300)
        )
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
        "expires_in": 300,
    }
    monkeypatch.setattr(requests, "post", lambda *a, **kw: success_response)
    kc.decode_token = Mock(return_value={"sub": "123"})

    create_token()
    assert get_token()._access_token == "new_token"
    assert get_token()._refresh_token == "new_refresh"


def test_device_flow_authorization_pending(monkeypatch):
    kc = keycloak_openid()
    kc.device = Mock(
        return_value={
            "device_code": "dev123",
            "user_code": "user123",
            "verification_uri": "http://verify",
            "verification_uri_complete": "http://verify?user=user123",
            "interval": 0,
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
        "expires_in": 300,
    }

    calls = iter([pending_response, success_response])
    monkeypatch.setattr(requests, "post", lambda *a, **kw: next(calls))
    kc.decode_token = Mock(return_value={"sub": "123"})

    create_token()
    assert get_token()._access_token == "token_ok"
    assert get_token()._refresh_token == "refresh_ok"


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

    with pytest.raises(AuthenticationError):
        create_token()


def test_register_resource_no_token():
    with pytest.raises(NotAuthenticatedError):
        aiod.datasets.register(metadata=dict(name="Foo"))


@responses.activate
def test_register_resource_invalid_token(invalid_refresh_token):
    with pytest.raises(AuthenticationError) as e:
        aiod.datasets.register(metadata=dict(name="Foo"))
    assert "is not valid" in str(e.value)


@responses.activate
def test_register_resource_expired_token(expired_refresh_token):
    with pytest.raises(AuthenticationError) as e:
        aiod.datasets.register(metadata=dict(name="Foo"))
    assert "is not valid" in str(e.value)


@responses.activate
def test_register_resource_valid_token(valid_refresh_token):
    responses.post(
        "http://not.set/not_set/datasets",
        json={"identifier": "data_123412341234123412341234"},
        match=[matchers.header_matcher({"Authorization": "Bearer valid_access"})],
    )
    identifier = aiod.datasets.register(metadata=dict(name="Foo"))
    assert identifier == "data_123412341234123412341234"


def test_token_to_file_creates_parent_directory(tmp_path):
    token_file = tmp_path / ".aiod" / "token.toml"
    assert not token_file.parent.exists()

    token = Token(refresh_token="abc")
    token.to_file(token_file)
    assert token_file.parent.exists() and token_file.parent.is_dir()
    assert token_file.exists() and token_file.is_file()

    # Calling it multiple times should not result in an error,
    # even if the directory or file already exist.
    token.to_file(token_file)


def test_malformed_token_file_logs_warning_and_does_not_crash(tmp_path, caplog):
    """Issue #223: a corrupt token.toml should NOT crash the import.

    The SDK should log a warning and fall back to unauthenticated mode
    (_token = None) so the user can still use public endpoints.

    We use importlib.reload() so the actual module-level loading block in
    authentication.py is exercised — not a copy of it.
    """
    import importlib

    # Create a token file with invalid TOML content
    bad_token_file = tmp_path / "token.toml"
    bad_token_file.write_text("{bad")  # malformed TOML

    original_token = authentication._token
    try:
        # Patch the module-level path and reload so the real boot-time block runs
        with patch.object(authentication, "_user_token_file", bad_token_file):
            with caplog.at_level(logging.WARNING, logger="aiod.authentication.authentication"):
                importlib.reload(authentication)

            # _token must be None — not an exception
            assert authentication._token is None, "_token should be None for a malformed file"
            # A warning must have been emitted
            assert any("Failed to load credentials" in r.message for r in caplog.records), \
                "Expected a warning about failed credential loading"
    finally:
        # Restore original token so other tests are not affected
        authentication._token = original_token
