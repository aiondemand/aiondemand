import responses

import aiod_sdk as aiod
from aiod_sdk.endpoints.endpoint import API_BASE_URL


def test_authorization_test():

    with responses.RequestsMock() as mocked_requests:
        mocked_requests.add(
            responses.GET,
            API_BASE_URL + "authorization_test",
            body=b'{"detail": "This endpoint requires authorization. You need to be logged in."}',
            status=401,
        )

        res = aiod.authorization_test()
        assert res.status_code == 401
        assert {
            "detail": "This endpoint requires authorization. You need to be logged in."
        } == res.json()
