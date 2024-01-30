import aiod_sdk


def test_version():
    assert aiod_sdk.__version__ == "0.1.0"


def test_hello_world():
    hello = aiod_sdk.aiod.get_hello_world()
    print(hello.json())
    assert type(hello.json()) is dict
