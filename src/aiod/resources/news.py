from dataclasses import dataclass
from aiod.calls import calls
from aiod.base.resource import BaseResource

@dataclass
class News(BaseResource):
    """Metadata for a News asset."""
    asset_type = "news"

    title: str | None = None
    content: str | None = None
    platform: str | None = None
    platform_resource_identifier: str | None = None
    date_published: str | None = None
    same_as: str | None = None
    keywords: list[str] | None = None

# --- Backward Compatibility API (Proxies to News classmethods) ---

def get_list(*args, **kwargs):
    """Retrieve a list of News assets."""
    return News.get_list(*args, **kwargs)

def counts(*args, **kwargs):
    """Retrieve the number of News assets."""
    return News.counts(*args, **kwargs)

def get_asset(*args, **kwargs):
    """Retrieve a specific News asset."""
    return News.get_asset(*args, **kwargs)

def register(*args, **kwargs):
    """Register a new News asset."""
    return News.register(*args, **kwargs)

def update(*args, **kwargs):
    """Update an existing News asset."""
    return News.update(*args, **kwargs)

def delete(*args, **kwargs):
    """Delete a News asset."""
    return News.delete(*args, **kwargs)

def get_asset_from_platform(*args, **kwargs):
    """Retrieve a News asset from an external platform."""
    return News.get_from_platform(*args, **kwargs)

def search(*args, **kwargs):
    """Search for News assets."""
    return News.search(*args, **kwargs)
