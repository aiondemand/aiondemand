from aiod import bookmarks, taxonomies
from aiod.authentication import create_token, get_current_user, invalidate_token
from aiod.calls.calls import get_any_asset as get
from aiod.configuration import config
from aiod.default.counts import asset_counts as counts
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

__version__ = "0.2.5"
