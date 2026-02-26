"""Base model package class."""

from importlib.metadata import PackageNotFoundError, version

from packaging.specifiers import InvalidSpecifier, SpecifierSet
from packaging.version import InvalidVersion, Version

from aiod.base import _BasePkg


class _AiodModelPkg(_BasePkg):
    _obj = None
    _obj_dict = {}
    _obj_presence = {}
    _obj_locations = {}

    def __init__(self, id=None):
        self.id = id
        super().__init__()

        pkg_id = self.get_tag("pkg_id")
        if pkg_id == "__multiple":
            self._obj = self._resolve_obj_for_id(id)

    @classmethod
    def _get_package_version(cls):
        """Return installed version of dependency package declared by ``pkg_pypi_name``."""
        pkg_name = cls.get_class_tag("pkg_pypi_name")
        if pkg_name in [None, "None"]:
            return None

        try:
            return Version(version(pkg_name))
        except (PackageNotFoundError, InvalidVersion):
            return None

    @staticmethod
    def _matches_specifier(package_version, specifier):
        """Return whether package version satisfies PEP 440 specifier string."""
        if specifier in [None, "", "*"]:
            return True
        if package_version is None:
            return False

        try:
            return package_version in SpecifierSet(specifier)
        except InvalidSpecifier:
            return False

    @classmethod
    def availability_range(cls, id):
        """Return PEP 440 availability range for estimator id, if declared."""
        return cls._obj_presence.get(id)

    @classmethod
    def location_rules(cls, id):
        """Return versioned location rules for estimator id, if declared."""
        return cls._obj_locations.get(id, [])

    @classmethod
    def is_available(cls, id, package_version=None):
        """Return whether estimator id is available for a package version."""
        presence_spec = cls.availability_range(id)
        if presence_spec is None:
            return True

        if package_version is None:
            package_version = cls._get_package_version()
        if isinstance(package_version, str):
            package_version = Version(package_version)

        return cls._matches_specifier(package_version, presence_spec)

    @classmethod
    def _resolve_obj_from_versioned_locations(cls, id, package_version):
        """Resolve object import location for id from versioned location metadata."""
        rules = cls.location_rules(id)
        if not rules:
            return None

        if isinstance(rules, dict):
            rules = [
                {"specifier": specifier, "obj": obj_loc}
                for specifier, obj_loc in rules.items()
            ]

        for rule in rules:
            if isinstance(rule, (tuple, list)) and len(rule) == 2:
                specifier, obj_loc = rule
            elif isinstance(rule, dict):
                specifier = rule.get("specifier")
                obj_loc = rule.get("obj")
            else:
                continue

            if cls._matches_specifier(package_version, specifier):
                return obj_loc

        return None

    @classmethod
    def _resolve_obj_for_id(cls, id):
        """Resolve import location for estimator id, considering version metadata."""
        if id is None:
            return None

        package_version = cls._get_package_version()
        if not cls.is_available(id=id, package_version=package_version):
            return None

        obj_loc = cls._resolve_obj_from_versioned_locations(
            id=id, package_version=package_version
        )
        if obj_loc is not None:
            return obj_loc

        return cls._obj_dict.get(id, None)

    @classmethod
    def contained_ids(cls):
        """Return list of ids of objects contained in this package.

        Returns
        -------
        ids : list of str
            list of unique identifiers of objects contained in this package
        """
        pkg_id = cls.get_class_tag("pkg_id")
        if pkg_id != "__multiple":
            return [cls.get_class_tag("pkg_id")]

        ids = set(cls._obj_dict.keys())
        ids.update(cls._obj_presence.keys())
        ids.update(cls._obj_locations.keys())

        return sorted(ids)

    def _materialize(self):
        pkg_obj = self.get_tag("pkg_obj")

        _obj = self._obj

        if _obj is None:
            raise ValueError(
                "Error in _AiodModelPkg._materialize. "
                "Either _materialize must be implemented, or"
                " the _obj attribute must be not None."
            )

        if pkg_obj == "reference":
            from skbase.utils.dependencies import _safe_import

            obj_loc = self._obj
            pkg_name = self.get_tag("pkg_pypi_name")

            return _safe_import(obj_loc, pkg_name=pkg_name)

        if pkg_obj == "code":
            exec(self._obj)

            return obj  # noqa: F821

        # elif pkg_obj == "craft":
        #    identify and call appropriate craft method

        raise ValueError(
            'Error in package tag "pkg_obj", '
            'must be one of "reference", "code", "craft", '
            f"but found value {pkg_obj}, of type {type(pkg_obj)}"
        )
