from unittest.mock import Mock

import pytest

import aiod
from aiod.configuration import config
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


def test_get_user_endpoint(mocked_token, httpx_mock):
    keycloak_openid().token = mocked_token

    httpx_mock.add_response(
        method="GET",
        url=f"{config.api_server}authorization_test",
        json={"name": "user", "roles": ["a_role"]},
    )
    set_token(
        Token(refresh_token="fake_refresh", access_token="fake_token", expires_in_seconds=300)
    )
    user = aiod.get_current_user()

    request = httpx_mock.get_requests()[0]
    assert request.headers["Authorization"] == "Bearer fake_token"
    assert user.name == "user", user
    assert user.roles == ("a_role",), user


def test_device_flow_success(httpx_mock):
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
    kc.decode_token = Mock(return_value={"sub": "123"})

    httpx_mock.add_response(
        method="POST",
        url="http://token",
        json={
            "access_token": "new_token",
            "refresh_token": "new_refresh",
            "expires_in": 300,
        },
    )

    create_token()
    assert get_token()._access_token == "new_token"
    assert get_token()._refresh_token == "new_refresh"


def test_device_flow_authorization_pending(httpx_mock):
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
    kc.decode_token = Mock(return_value={"sub": "123"})

    httpx_mock.add_response(
        method="POST",
        url="http://token",
        json={"error": "authorization_pending"},
        status_code=400,
    )
    httpx_mock.add_response(
        method="POST",
        url="http://token",
        json={
            "access_token": "token_ok",
            "refresh_token": "refresh_ok",
            "expires_in": 300,
        },
    )

    create_token()
    assert get_token()._access_token == "token_ok"
    assert get_token()._refresh_token == "refresh_ok"


def test_device_flow_failure(httpx_mock):
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

    httpx_mock.add_response(
        method="POST",
        url="http://token",
        json={"error": "expired_token"},
        status_code=400,
    )

    with pytest.raises(AuthenticationError):
        create_token()


def test_register_resource_no_token():
    with pytest.raises(NotAuthenticatedError):
        aiod.datasets.register(metadata=dict(name="Foo"))


def test_register_resource_invalid_token(invalid_refresh_token):
    with pytest.raises(AuthenticationError) as e:
        aiod.datasets.register(metadata=dict(name="Foo"))
    assert "is not valid" in str(e.value)


def test_register_resource_expired_token(expired_refresh_token):
    with pytest.raises(AuthenticationError) as e:
        aiod.datasets.register(metadata=dict(name="Foo"))
    assert "is not valid" in str(e.value)


def test_register_resource_valid_token(valid_refresh_token, httpx_mock):
    httpx_mock.add_response(
        method="POST",
        url="http://not.set/not_set/datasets",
        match_headers={"Authorization": "Bearer valid_access"},
        json={"identifier": "data_123412341234123412341234"},
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
