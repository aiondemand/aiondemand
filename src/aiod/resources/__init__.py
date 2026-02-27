from .base_resource import BaseResource, SearchableMixin
from .case_studies import CaseStudies
from .computational_assets import ComputationalAssets
from .contacts import Contacts
from .datasets import Datasets
from .educational_resources import EducationalResources
from .events import Events
from .experiments import Experiments
from .ml_models import MLModels
from .news import News
from .organisations import Organisations
from .persons import Persons
from .platforms import Platforms
from .projects import Projects
from .publications import Publications
from .services import Services
from .teams import Teams


# Mapping from asset type name (as used in API) to class instance
class Resources:
    case_studies = CaseStudies()
    computational_assets = ComputationalAssets()
    contacts = Contacts()
    datasets = Datasets()
    educational_resources = EducationalResources()
    events = Events()
    experiments = Experiments()
    ml_models = MLModels()
    news = News()
    organisations = Organisations()
    persons = Persons()
    platforms = Platforms()
    projects = Projects()
    publications = Publications()
    services = Services()
    teams = Teams()
