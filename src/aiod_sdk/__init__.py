from importlib.metadata import version
from aiod_sdk import aiod
from aiod_sdk.endpoints.authorization_test import AuthorizationTest
from aiod_sdk.endpoints.counts import Counts

authorization_test = AuthorizationTest.test
counts = Counts.asset_counts

__version__ = version(__name__)
