from aiod.calls import calls

(
    get_list,
    counts,
    get_asset,
    post_asset,
    put_asset,
    delete_asset,
    get_asset_from_platform,
    get_content,
    get_assets_async,
    get_list_async,
) = calls.wrap_common_calls(asset_type="datasets", module=__name__)

(search,) = calls.wrap_search_call(asset_type="datasets", module=__name__)
