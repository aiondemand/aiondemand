from dataclasses import dataclass
from aiod.calls import calls
from aiod.base.resource import BaseResource

@dataclass
class Organisation(BaseResource):
    """Metadata for an Organisation asset."""
    asset_type = "organisations"

    name: str | None = None
    description: str | None = None
    platform: str | None = None
    platform_resource_identifier: str | None = None
    date_published: str | None = None
    same_as: str | None = None
    type: str | None = None

# --- Backward Compatibility API (Proxies to Organisation classmethods) ---

def get_list(*args, **kwargs):
    """Retrieve a list of Organisation assets."""
    return Organisation.get_list(*args, **kwargs)

def counts(*args, **kwargs):
    """Retrieve the number of Organisation assets."""
    return Organisation.counts(*args, **kwargs)

def get_asset(*args, **kwargs):
    """Retrieve a specific Organisation asset."""
    return Organisation.get_asset(*args, **kwargs)

def register(*args, **kwargs):
    """Register a new Organisation asset."""
    return Organisation.register(*args, **kwargs)

def update(*args, **kwargs):
    """Update an existing Organisation asset."""
    return Organisation.update(*args, **kwargs)

def delete(*args, **kwargs):
    """Delete an Organisation asset."""
    return Organisation.delete(*args, **kwargs)

def get_asset_from_platform(*args, **kwargs):
    """Retrieve an Organisation asset from an external platform."""
    return Organisation.get_from_platform(*args, **kwargs)

def search(*args, **kwargs):
    """Search for Organisation assets."""
    return Organisation.search(*args, **kwargs)
