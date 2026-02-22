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

(
    get_list,
    counts,
    get_asset,
    register,
    replace,
    update,
    delete,
    get_asset_from_platform,
    get_content,
    get_assets_async,
    get_list_async,
) = calls.wrap_common_calls(asset_type="news", module=__name__)

(search,) = calls.wrap_search_call(asset_type="news", module=__name__)
