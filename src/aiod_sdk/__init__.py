from importlib.metadata import version
from aiod_sdk import aiod
from aiod_sdk.endpoints.authorization_test import AuthorizationTest
from aiod_sdk.endpoints.counts import Counts
from aiod_sdk.endpoints.platforms import Platforms
from aiod_sdk.endpoints.case_studies import CaseStudies
from aiod_sdk.endpoints.computational_assets import ComputationalAssets

__version__ = version(__name__)

authorization_test = AuthorizationTest.test
counts = Counts.asset_counts
platforms = Platforms
case_studies = CaseStudies
computational_assets = ComputationalAssets
