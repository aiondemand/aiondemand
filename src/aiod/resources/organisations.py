from aiod.resources.base_resource import BaseResource, SearchableMixin


class Organisations(SearchableMixin, BaseResource):
    asset_type = "organisations"
