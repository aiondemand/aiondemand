import pytest
import responses

from unittest.mock import Mock

import aiod
from aiod.configuration import config
from aiod.authentication.authentication import keycloak_openid


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
