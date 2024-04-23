from aiod_sdk.calls import calls

(
    get_list,
    counts,
    get_asset,
    get_asset_from_platform,
    get_content,
    get_asset_async,
    get_list_async,
) = calls.wrap_common_calls(asset_type="datasets")

(search,) = calls.wrap_search_call(asset_type="datasets")
