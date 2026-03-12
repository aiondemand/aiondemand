from aiod.resources.base_resource import BaseResource, SearchableMixin


class Publications(SearchableMixin, BaseResource):
    asset_type = "publications"
