from aiod_sdk.calls import calls

get_list, counts, get_asset, get_assets_async, get_list_async = calls.wrap_common_calls(
    asset_type="events"
)
