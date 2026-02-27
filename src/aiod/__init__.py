from aiod.configuration import config
from aiod import taxonomies
from aiod import bookmarks
from aiod.resources import (
    BaseResource,
    SearchableMixin,
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
    Services,
    Teams,
)

from aiod.authentication import invalidate_token, get_current_user, create_token
from aiod.default.counts import asset_counts as counts
from aiod.calls.calls import get_any_asset as get
from aiod.__version__ import version


def __getattr__(name: str):
    """Forward attribute access to resources module for backwards compatibility.

    This allows `aiod.datasets.get_list()` to work by forwarding to
    `aiod.resources.datasets` which returns a singleton instance.
    """
    import aiod.resources as resources
    if hasattr(resources,name):
        return getattr(resources, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
