from importlib.metadata import version
from aiod.config.config import set_api_base_url, set_authentication_server, show_config
from aiod.default.authorization_test import test as authorization_test
from aiod.default.counts import asset_counts as counts
from aiod.resources import case_studies
from aiod.resources import computational_assets
from aiod.resources import contacts
from aiod.resources import datasets
from aiod.resources import educational_resources
from aiod.resources import events
from aiod.resources import experiments
from aiod.resources import ml_models
from aiod.resources import news
from aiod.resources import organisations
from aiod.resources import persons
from aiod.resources import platforms
from aiod.resources import projects
from aiod.resources import publications
from aiod.resources import services
from aiod.resources import teams

__version__ = version(__name__)
