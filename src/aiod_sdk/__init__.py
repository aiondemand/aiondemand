from importlib.metadata import version
from aiod_sdk import aiod
from aiod_sdk.endpoints.authorization_test import AuthorizationTest

authorization_test = AuthorizationTest.authorization_test
__version__ = version(__name__)
