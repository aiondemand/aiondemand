from importlib.metadata import version
from aiod_sdk import aiod
from aiod_sdk.endpoints.authorization_test import AuthorizationTest
from aiod_sdk.endpoints.case_studies import CaseStudies
from aiod_sdk.endpoints.computational_assets import ComputationalAssets
from aiod_sdk.endpoints.contacts import Contacts
from aiod_sdk.endpoints.counts import Counts
from aiod_sdk.endpoints.datasets import Datasets
from aiod_sdk.endpoints.educational_resources import EducationalResources
from aiod_sdk.endpoints.events import Events
from aiod_sdk.endpoints.experiments import Experiments
from aiod_sdk.endpoints.ml_models import MLModels
from aiod_sdk.endpoints.news import News
from aiod_sdk.endpoints.organisations import Organisations
from aiod_sdk.endpoints.persons import Persons
from aiod_sdk.endpoints.platforms import Platforms
from aiod_sdk.endpoints.projects import Projects
from aiod_sdk.endpoints.publications import Publications
from aiod_sdk.endpoints.services import Services
from aiod_sdk.endpoints.teams import Teams

__version__ = version(__name__)

authorization_test = AuthorizationTest.test
case_studies = CaseStudies
computational_assets = ComputationalAssets
contacts = Contacts
counts = Counts.asset_counts
datasets = Datasets
educational_resources = EducationalResources
events = Events
experiments = Experiments
ml_models = MLModels
news = News
organisations = Organisations
persons = Persons
platforms = Platforms
projects = Projects
publications = Publications
services = Services
teams = Teams
