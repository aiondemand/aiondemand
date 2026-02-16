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

# Mapping from asset type name (as used in API) to class
_asset_classes = {
    "case_studies": CaseStudies,
    "computational_assets": ComputationalAssets,
    "contacts": Contacts,
    "datasets": Datasets,
    "educational_resources": EducationalResources,
    "events": Events,
    "experiments": Experiments,
    "ml_models": MLModels,
    "news": News,
    "organisations": Organisations,
    "persons": Persons,
    "platforms": Platforms,
    "projects": Projects,
    "publications": Publications,
    "services": Services,
    "teams": Teams,
}

# Cache for singleton instances
_instances: dict[str, BaseResource] = {}


def __getattr__(name: str):
    """Redirect attribute access to class instances for backwards compatibility.

    This allows `aiod.resources.datasets.get_list()` to work by returning
    a singleton instance of the Datasets class.
    """
    if name in _asset_classes:
        if name not in _instances:
            _instances[name] = _asset_classes[name]()
        return _instances[name]
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


# Override module imports with class instances for backwards compatibility
# This ensures that resources.datasets returns an instance, not the module
for asset_name, asset_class in _asset_classes.items():
    _instances[asset_name] = asset_class()
    # Set in __dict__
    globals()[asset_name] = _instances[asset_name]
