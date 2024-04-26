from importlib.metadata import version
from aiod_sdk.default.authorization_test import test as authorization_test
from aiod_sdk.resources import case_studies
from aiod_sdk.resources import computational_assets
from aiod_sdk.resources import contacts
from aiod_sdk.default.counts import asset_counts as counts
from aiod_sdk.resources import datasets
from aiod_sdk.resources import educational_resources
from aiod_sdk.resources import events
from aiod_sdk.resources import experiments
from aiod_sdk.resources import ml_models
from aiod_sdk.resources import news
from aiod_sdk.resources import organisations
from aiod_sdk.resources import persons
from aiod_sdk.resources import platforms
from aiod_sdk.resources import projects
from aiod_sdk.resources import publications
from aiod_sdk.resources import services
from aiod_sdk.resources import teams

__version__ = version(__name__)
