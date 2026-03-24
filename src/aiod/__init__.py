from aiod import bookmarks, taxonomies
from aiod.authentication import create_token, get_current_user, invalidate_token
from aiod.automation import (
    get_paper,
    list_cached_papers,
    populate_paper_from_pdf,
)

# from aiod.calls.calls import get_any_asset as get
from aiod.configuration import config
from aiod.default.counts import asset_counts as counts
from aiod.models import get as _models_get
from aiod.resources import (
    case_studies,
    computational_assets,
    contacts,
    datasets,
    educational_resources,
    events,
    experiments,
    ml_models,
    news,
    organisations,
    persons,
    platforms,
    projects,
    publications,
    services,
    teams,
)

__all__ = [
    "config",
    "taxonomies",
    "bookmarks",
    "case_studies",
    "computational_assets",
    "contacts",
    "datasets",
    "educational_resources",
    "events",
    "experiments",
    "ml_models",
    "news",
    "organisations",
    "persons",
    "platforms",
    "projects",
    "publications",
    "services",
    "teams",
    "invalidate_token",
    "get_current_user",
    "create_token",
    "counts",
    "get",
    "get_paper",
    "populate_paper_from_pdf",
    "list_cached_papers",
]


def get(id: str):
    """Resolve top-level get: DOI-based paper retrieval or existing model retrieval."""
    if isinstance(id, str) and id.strip().lower().startswith("doi:"):
        return get_paper(id.strip())
    return _models_get(id)


# def __getattr__(name: str):
#     if name in __all__:
#         return globals()[name]
#     if name not in __all__:
#         return get(name)
#     return None

__version__ = "0.2.5"
