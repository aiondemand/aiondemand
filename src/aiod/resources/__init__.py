from .base_resource import BaseResource, SearchableMixin
from .contacts import Contacts
from .datasets import Datasets
from .organisations import Organisations
from .projects import Projects
from .platforms import Platforms
from .services import Services
from .news import News
from .experiments import Experiments
from .events import Events
from .educational_resources import EducationalResources
from .computational_assets import ComputationalAssets
from .ml_models import MLModels
from .persons import Persons
from .teams import Teams
from .publications import Publications
from .case_studies import CaseStudies

# Mapping from asset type name (as used in API) to class instance
case_studies =  CaseStudies()
computational_assets = ComputationalAssets()
contacts =  Contacts()
datasets = Datasets()
educational_resources =  EducationalResources()
events =  Events()
experiments = Experiments()
ml_models = MLModels()
news = News()
organisations = Organisations()
persons = Persons()
platforms =  Platforms()
projects = Projects()
publications = Publications()
services = Services()
teams = Teams()
