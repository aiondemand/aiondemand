from dataclasses import dataclass
from aiod.calls import calls
from aiod.base.resource import BaseResource

@dataclass
class Publication(BaseResource):
    """Metadata for a Publication asset."""
    asset_type = "publications"

    name: str | None = None
    description: str | None = None
    platform: str | None = None
    platform_resource_identifier: str | None = None
    date_published: str | None = None
    same_as: str | None = None
    type: str | None = None
    issn: str | None = None

# --- Backward Compatibility API (Proxies to Publication classmethods) ---

def get_list(*args, **kwargs):
    """Retrieve a list of Publication assets."""
    return Publication.get_list(*args, **kwargs)

def counts(*args, **kwargs):
    """Retrieve the number of Publication assets."""
    return Publication.counts(*args, **kwargs)

def get_asset(*args, **kwargs):
    """Retrieve a specific Publication asset."""
    return Publication.get_asset(*args, **kwargs)

def register(*args, **kwargs):
    """Register a new Publication asset."""
    return Publication.register(*args, **kwargs)

def update(*args, **kwargs):
    """Update an existing Publication asset."""
    return Publication.update(*args, **kwargs)

def delete(*args, **kwargs):
    """Delete a Publication asset."""
    return Publication.delete(*args, **kwargs)

def get_asset_from_platform(*args, **kwargs):
    """Retrieve a Publication asset from an external platform."""
    return Publication.get_from_platform(*args, **kwargs)

def search(*args, **kwargs):
    """Search for Publication assets."""
    return Publication.search(*args, **kwargs)
