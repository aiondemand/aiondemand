import aiod_sdk as aiod


def test_authorization_test():
    res = aiod.authorization_test()

    assert res.status_code == 401
    assert {
        "detail": "This endpoint requires authorization. You need to be logged in."
    } == res.json()
