from aiod.resources.base_resource import BaseResource, SearchableMixin


class Services(SearchableMixin, BaseResource):
    asset_type = "services"
