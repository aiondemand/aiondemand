from aiod import bookmarks, taxonomies
from aiod.authentication import create_token, get_current_user, invalidate_token
from aiod.configuration import config
from aiod.default.counts import asset_counts as counts
from aiod.models import get
from aiod.resources import (
    BaseResource,
    CaseStudies,
    ComputationalAssets,
    Contacts,
    Datasets,
    EducationalResources,
    Events,
    Experiments,
    MLModels,
    News,
    Organisations,
    Persons,
    Platforms,
    Projects,
    Publications,
    SearchableMixin,
    Services,
    Teams,
)

__all__ = [
    "bookmarks",
    "taxonomies",
    "config",
    "create_token",
    "get_current_user",
    "invalidate_token",
    "counts",
    "get",
    "BaseResource",
    "SearchableMixin",
    "CaseStudies",
    "ComputationalAssets",
    "Contacts",
    "Datasets",
    "EducationalResources",
    "Events",
    "Experiments",
    "MLModels",
    "News",
    "Organisations",
    "Persons",
    "Platforms",
    "Projects",
    "Publications",
    "Services",
    "Teams",
    "__version__",
]


def __getattr__(name: str):
    """Forward attribute access to resources module for backwards compatibility.

    This allows `aiod.datasets.get_list()` to work by forwarding to
    `aiod.resources.datasets` which returns a singleton instance.
    """
    from aiod.resources import Resources

    _resources = Resources()
    if hasattr(_resources, name):
        return getattr(_resources, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


# def __getattr__(name: str):
#     if name in __all__:
#         return globals()[name]
#     if name not in __all__:
#         return get(name)
#     return None

__version__ = "0.2.5"
