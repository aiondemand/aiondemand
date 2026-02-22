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
) = calls.wrap_common_calls(asset_type="ml_models", module=__name__)

(search,) = calls.wrap_search_call(asset_type="ml_models", module=__name__)
