from aiod.resources.base_resource import BaseResource, SearchableMixin


class Experiments(SearchableMixin, BaseResource):
    asset_type = "experiments"
