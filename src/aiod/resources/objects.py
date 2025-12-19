from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass
class Asset:
    """Lightweight Python object wrapper around an AIoD asset payload.

    Notes
    -----
    - Provides attribute-style access to top-level keys of the underlying dict.
    - Keeps the original payload accessible via ``to_dict()``.
    - Stores the ``asset_type`` for context and tries to expose ``identifier``
      if present in the payload (either at top-level or under ``aiod_entry``).
    """

    asset_type: str | None
    data: Mapping[str, Any]

    def __post_init__(self) -> None:
        # Best-effort identifier extraction for convenience
        aiod_entry = self.data.get("aiod_entry") if isinstance(self.data, dict) else None
        self.identifier = (
            (self.data.get("identifier") if isinstance(self.data, dict) else None)
            or (aiod_entry.get("identifier") if isinstance(aiod_entry, dict) else None)
        )

    def __getattr__(self, item: str) -> Any:
        # Delegate missing attributes to the underlying mapping for dot-access
        if isinstance(self.data, dict) and item in self.data:
            return self.data[item]
        available = list(self.data) if isinstance(self.data, dict) else []
        raise AttributeError(
            f"{item!r} not found on Asset; available keys: {available}"
        )

    def to_dict(self) -> dict:
        """Return the underlying JSON-compatible dictionary payload."""
        return dict(self.data) if isinstance(self.data, dict) else dict(self.data.items())

    @classmethod
    def from_dict(cls, asset_type: str | None, payload: Mapping[str, Any]) -> "Asset":
        return cls(asset_type=asset_type, data=payload)

    def __repr__(self) -> str:  # pragma: no cover - human-friendly representation
        ident = f" id={self.identifier!r}" if getattr(self, "identifier", None) else ""
        at = f" {self.asset_type}" if self.asset_type else ""
        return f"<Asset{at}{ident}>"
