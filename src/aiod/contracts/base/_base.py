"""Base class for API contracts."""

from typing import Any

from skbase.base import BaseObject

from aiod.contracts.utils import ContractError


class _BaseContract(BaseObject):
    _tags = {
        "object_type": "contract",
        "short_descr": "basic scitype for all contracts",
    }

    @classmethod
    def istypeof(cls, obj: Any) -> bool:
        """Return True if object satisfies this contract."""
        obj = cls._resolve(obj)

        try:
            return cls._check_structure(obj)
        except ContractError:
            return False

    @classmethod
    def runtests(cls, identifier: str | type) -> dict:
        """Run contract tests and return summary."""
        results = {
            "contract": cls.__name__,
            "target": str(identifier),
            "passed": True,
            "errors": [],
        }
        obj = cls._resolve(identifier)

        try:
            cls._check_structure(obj)
            cls._run_behavioral_tests(obj)
        except Exception as e:
            results["passed"] = False
            results["errors"].append(str(e))

        return results

    @classmethod
    def _resolve(cls, obj: Any) -> Any:
        """Resolve identifier to class."""
        if isinstance(obj, str):
            from aiod import get

            return get(obj)
        return obj

    @classmethod
    def _check_structure(cls, obj: type) -> bool:
        raise RuntimeError("abstract method")

    @classmethod
    def _run_behavioral_tests(cls, obj: type):
        raise RuntimeError("abstract method")


__all__ = ["_BaseContract"]
