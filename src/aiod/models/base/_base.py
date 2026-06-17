"""Base model package class."""

from packaging.specifiers import InvalidSpecifier, SpecifierSet
from packaging.version import Version
from skbase.utils.dependencies import _check_soft_dependencies
from skbase.utils.dependencies._dependencies import _get_pkg_version

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
        """Return installed version for package in ``pkg_pypi_name``.

        Returns
        -------
        Version or None
            Installed package version as ``packaging.version.Version``,
            or ``None`` if package is undefined or unavailable.
        """
        pkg_name = cls.get_class_tag("pkg_pypi_name")
        if pkg_name in [None, "None"]:
            return None

        return _get_pkg_version(pkg_name)

    @staticmethod
    def _matches_specifier(package_version, specifier):
        """Return whether package version satisfies PEP 440 specifier.

        Parameters
        ----------
        package_version : Version or str or None
            Package version to check against ``specifier``.
        specifier : str or None
            PEP 440 version range expression.

        Returns
        -------
        bool
            Whether ``package_version`` matches ``specifier``.
        """
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
        """Return declared availability specifier for estimator id.

        Parameters
        ----------
        id : str
            Estimator identifier.

        Returns
        -------
        str or None
            PEP 440 specifier string from ``_obj_presence`` for ``id``,
            or ``None`` if no range is declared.
        """
        return cls._obj_presence.get(id)

    @classmethod
    def location_rules(cls, id):
        """Return declared versioned location rules for estimator id.

        Parameters
        ----------
        id : str
            Estimator identifier.

        Returns
        -------
        list or dict
            Versioned location rules from ``_obj_locations`` for ``id``,
            or an empty list if no rules are declared.
        """
        return cls._obj_locations.get(id, [])

    @classmethod
    def is_available(cls, id, package_version=None):
        """Return whether estimator id is available for a package version.

        Parameters
        ----------
        id : str
            Estimator identifier.
        package_version : Version or str or None, optional
            Version to evaluate against availability range. If ``None``,
            the installed version of ``pkg_pypi_name`` is used.

        Returns
        -------
        bool
            Whether estimator ``id`` is available for the resolved version.
        """
        presence_spec = cls.availability_range(id)
        if presence_spec is None:
            return True

        pkg_name = cls.get_class_tag("pkg_pypi_name")

        if package_version is None:
            if pkg_name in [None, "None"]:
                return False
            req = f"{pkg_name}{presence_spec}"
            return _check_soft_dependencies(req, severity="none")
        if isinstance(package_version, str):
            package_version = Version(package_version)

        return cls._matches_specifier(package_version, presence_spec)

    @classmethod
    def _resolve_obj_from_versioned_locations(cls, id, package_version):
        """Resolve object import path for id from versioned location metadata.

        Parameters
        ----------
        id : str
            Estimator identifier.
        package_version : Version or str or None
            Package version used to select matching location rule.

        Returns
        -------
        str or None
            Matching import path, or ``None`` if no rule matches.
        """
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
        """Resolve import path for estimator id using version-aware metadata.

        Parameters
        ----------
        id : str
            Estimator identifier.

        Returns
        -------
        str or None
            Resolved import path if available, otherwise ``None``.
        """
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
        return list(cls._obj_dict.keys())

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
