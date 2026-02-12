from aiod.resources.base_resource import BaseResource, SearchableMixin


class News(SearchableMixin, BaseResource):
    asset_type = "news"
