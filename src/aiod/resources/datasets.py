
from aiod.resources.base_resource import BaseResource, SearchableMixin

class Datasets(SearchableMixin, BaseResource):
    asset_type = "datasets"

