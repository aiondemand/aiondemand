from dataclasses import dataclass
from aiod.calls import calls
from aiod.base.resource import BaseResource

@dataclass
class MLModel(BaseResource):
    """Metadata for an ML Model asset."""
    asset_type = "ml_models"

    name: str | None = None
    description: str | None = None
    platform: str | None = None
    platform_resource_identifier: str | None = None
    date_published: str | None = None
    same_as: str | None = None
    is_accessible_for_free: bool | None = None
    version: str | None = None
    keywords: list[str] | None = None

# --- Backward Compatibility API (Proxies to MLModel classmethods) ---

def get_list(*args, **kwargs):
    """Retrieve a list of MLModel assets."""
    return MLModel.get_list(*args, **kwargs)

def counts(*args, **kwargs):
    """Retrieve the number of MLModel assets."""
    return MLModel.counts(*args, **kwargs)

def get_asset(*args, **kwargs):
    """Retrieve a specific MLModel asset."""
    return MLModel.get_asset(*args, **kwargs)

def register(*args, **kwargs):
    """Register a new MLModel asset."""
    return MLModel.register(*args, **kwargs)

def update(*args, **kwargs):
    """Update an existing MLModel asset."""
    return MLModel.update(*args, **kwargs)

def delete(*args, **kwargs):
    """Delete an MLModel asset."""
    return MLModel.delete(*args, **kwargs)

def get_asset_from_platform(*args, **kwargs):
    """Retrieve an MLModel asset from an external platform."""
    return MLModel.get_from_platform(*args, **kwargs)

def search(*args, **kwargs):
    """Search for MLModel assets."""
    return MLModel.search(*args, **kwargs)

# Note: Async methods can be added similarly if needed.
