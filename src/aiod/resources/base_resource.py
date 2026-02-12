from aiod.calls import calls

class BaseResource:
    asset_type: str

    def __init__(self):
        pass

    def list(self, *, platform=None, offset=0, limit=10, version=None, data_format="pandas"):
        return calls.get_list(asset_type=self.asset_type, platform=platform, offset=offset, limit=limit, version=version, data_format=data_format)

    def counts(self, *, version=None, per_platform=False):
        return calls.counts(asset_type=self.asset_type, version=version, per_platform=per_platform)

    def get(self, identifier, *, version=None, data_format="pandas"):
        return calls.get_asset(identifier, asset_type=self.asset_type, version=version, data_format=data_format)

    def register(self, metadata, *, version=None):
        return calls.post_asset(asset_type=self.asset_type, metadata=metadata, version=version)

    def replace(self, identifier, metadata, *, version=None):
        return calls.put_asset(asset_type=self.asset_type, identifier=identifier, metadata=metadata, version=version)

    def update(self, identifier, metadata, *, version=None):
        return calls.patch_asset(asset_type=self.asset_type, identifier=identifier, metadata=metadata, version=version)

    def delete(self, identifier, *, version=None):
        return calls.delete_asset(asset_type=self.asset_type, identifier=identifier, version=version)

    def get_from_platform(self, *, platform, platform_identifier, version=None, data_format="pandas"):
        return calls.get_asset_from_platform(platform=platform, platform_identifier=platform_identifier, asset_type=self.asset_type, version=version, data_format=data_format)

    def content(self, identifier, *, distribution_idx=0, version=None):
        return calls.get_content(asset_type=self.asset_type, identifier=identifier, distribution_idx=distribution_idx, version=version)

    def get_assets_async(self, identifiers, *, version=None, data_format="pandas"):
        return calls.get_assets_async(identifiers, asset_type=self.asset_type, version=version, data_format=data_format)

    def get_list_async(self, *, offset=0, limit=100, batch_size=10, version=None, data_format="pandas"):
        return calls.get_list_async(asset_type=self.asset_type, offset=offset, limit=limit, batch_size=batch_size, version=version, data_format=data_format)


class SearchableMixin:
    def search(self, query, *, platforms=None, offset=0, limit=10, search_field=None, get_all=True, version=None, data_format="pandas"):
        return calls.search(query, asset_type=self.asset_type, platforms=platforms, offset=offset, limit=limit, search_field=search_field, get_all=get_all, version=version, data_format=data_format)