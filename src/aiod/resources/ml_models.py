from aiod.resources.base_resource import BaseResource, SearchableMixin


class MLModels(SearchableMixin, BaseResource):
    asset_type = "ml_models"
