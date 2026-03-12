from aiod.resources.base_resource import BaseResource, SearchableMixin


class Projects(SearchableMixin, BaseResource):
    asset_type = "projects"
