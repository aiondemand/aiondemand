"""Base class for API contracts."""

from __future__ import annotations

from typing import Any, Dict, Type

from aiod.base import _BasePkg


class BaseAPIContract(_BasePkg):
    """Base class for API contracts.

    API contracts define structural and behavioral constraints
    that an object must satisfy to inhabit the contract.
    """

    _tags: Dict[str, Any] = {
        "contract_type": None,
        "maintainers": ["aiod developers"],
        "python_dependencies": None,
        "pkg_id": None,
        "pkg_obj": "reference",
        "pkg_obj_type": "api_contract",
    }

    @classmethod
    def isinhabitant(cls, identifier: str | Type) -> bool:
        """Return True if object satisfies this contract."""
        try:
            obj = cls._resolve(identifier)
        except Exception:
            return False

        try:
            return cls._check_structure(obj)
        except Exception:
            return False

    @classmethod
    def runtests(cls, identifier: str | Type) -> dict:
        """Run contract tests and return summary."""
        obj = cls._resolve(identifier)

        results = {
            "contract": cls.__name__,
            "target": getattr(obj, "__name__", str(obj)),
            "passed": True,
            "errors": [],
        }

        try:
            cls._check_structure(obj)
        except Exception as e:
            results["passed"] = False
            results["errors"].append(str(e))

        try:
            cls._run_behavioral_tests(obj)
        except Exception as e:
            results["passed"] = False
            results["errors"].append(str(e))

        return results

    @classmethod
    def _resolve(cls, identifier: str | Type):
        """Resolve identifier to class."""
        if isinstance(identifier, str):
            from aiod import get

            return get(identifier)
        return identifier

    @classmethod
    def _check_structure(cls, obj: Type) -> bool:
        raise RuntimeError("abstract method")

    @classmethod
    def _run_behavioral_tests(cls, obj: Type):
        raise RuntimeError("abstract method")
