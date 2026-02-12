from aiod.resources.base_resource import BaseResource, SearchableMixin


class Events(SearchableMixin, BaseResource):
    asset_type = "events"
