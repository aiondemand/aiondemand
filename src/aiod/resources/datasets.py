from dataclasses import dataclass
from aiod.calls import calls
from aiod.base.resource import BaseResource

@dataclass
class Dataset(BaseResource):
    """Metadata for a Dataset asset."""
    asset_type = "datasets"

    name: str | None = None
    description: str | None = None
    platform: str | None = None
    platform_resource_identifier: str | None = None
    date_published: str | None = None
    same_as: str | None = None
    is_accessible_for_free: bool | None = None
    version: str | None = None
    keywords: list[str] | None = None

# --- Backward Compatibility API (Proxies to Dataset classmethods) ---

def get_list(*args, **kwargs):
    """Retrieve a list of Dataset assets."""
    return Dataset.get_list(*args, **kwargs)

def counts(*args, **kwargs):
    """Retrieve the number of Dataset assets."""
    return Dataset.counts(*args, **kwargs)

def get_asset(*args, **kwargs):
    """Retrieve a specific Dataset asset."""
    return Dataset.get_asset(*args, **kwargs)

def register(*args, **kwargs):
    """Register a new Dataset asset."""
    return Dataset.register(*args, **kwargs)

def update(*args, **kwargs):
    """Update an existing Dataset asset."""
    return Dataset.update(*args, **kwargs)

def delete(*args, **kwargs):
    """Delete a Dataset asset."""
    return Dataset.delete(*args, **kwargs)

def get_asset_from_platform(*args, **kwargs):
    """Retrieve a Dataset asset from an external platform."""
    return Dataset.get_from_platform(*args, **kwargs)

def search(*args, **kwargs):
    """Search for Dataset assets."""
    return Dataset.search(*args, **kwargs)

# Note: Async methods can be added similarly if needed.
