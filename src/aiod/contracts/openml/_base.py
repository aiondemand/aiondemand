"""Base class for openml API contracts."""

from aiod.contracts.base import _BaseContract

__all__ = ["_BaseOpenMLContract"]


class _BaseOpenMLContract(_BaseContract):
    _tags = {
        "python_dependencies": "openml",
        "pkg_pypi_name": "openml",
        "scitype_name": "openml",
        "short_descr": "basic scitype for all openml contracts",
    }
