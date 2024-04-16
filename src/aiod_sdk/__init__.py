from importlib.metadata import version
from aiod_sdk.endpoints.authorization_test import test as authorization_test
from aiod_sdk.endpoints import case_studies
from aiod_sdk.endpoints import computational_assets
from aiod_sdk.endpoints import contacts
from aiod_sdk.endpoints.counts import asset_counts as counts
from aiod_sdk.endpoints import datasets
from aiod_sdk.endpoints import educational_resources
from aiod_sdk.endpoints import events
from aiod_sdk.endpoints import experiments
from aiod_sdk.endpoints import ml_models
from aiod_sdk.endpoints import news
from aiod_sdk.endpoints import organisations
from aiod_sdk.endpoints import persons
from aiod_sdk.endpoints import platforms
from aiod_sdk.endpoints import projects
from aiod_sdk.endpoints import publications
from aiod_sdk.endpoints import services
from aiod_sdk.endpoints import teams

__version__ = version(__name__)
