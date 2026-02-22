from __future__ import annotations

import dataclasses
from typing import Any, ClassVar, TypeVar, TYPE_CHECKING, Literal

if TYPE_CHECKING:
    import pandas as pd

T = TypeVar("T", bound="BaseResource")

@dataclasses.dataclass
class BaseResource:
    """Base class for all AI-on-Demand metadata resources.

    This class provides a common interface for interacting with metadata assets
    defined in the AI-on-Demand catalogue. Subclasses should define the specific
    fields available for each asset type.
    """

    asset_type: ClassVar[str] = ""
    identifier: str | None = None

    @classmethod
    def get(cls: type[T], identifier: str) -> T:
        """Retrieve a specific resource by its identifier."""
        from aiod.calls.calls import get_asset
        data = get_asset(identifier, asset_type=cls.asset_type, data_format="json")
        return cls._from_dict(data)

    @classmethod
    def list(
        cls: type[T],
        offset: int = 0,
        limit: int = 10,
        platform: str | None = None,
    ) -> list[T]:
        """Retrieve a list of resources."""
        from aiod.calls.calls import get_list
        data = get_list(
            asset_type=cls.asset_type,
            offset=offset,
            limit=limit,
            platform=platform,
            data_format="json",
        )
        return [cls._from_dict(item) for item in data]

    @classmethod
    def counts(cls) -> int | dict[str, int]:
        """Retrieve the number of resources in the metadata catalogue."""
        from aiod.calls.calls import counts
        return counts(asset_type=cls.asset_type)

    def save(self) -> None:
        """Save the resource to the catalogue (register or update)."""
        if self.identifier:
            from aiod.calls.calls import patch_asset
            # Best effort patch logic
            patch_asset(
                asset_type=self.asset_type,
                identifier=self.identifier,
                metadata=self.to_dict(),
            )
        else:
            from aiod.calls.calls import post_asset
            self.identifier = post_asset(
                asset_type=self.asset_type,
                metadata=self.to_dict(),
            )

    def delete(self) -> None:
        """Delete the resource from the catalogue."""
        if not self.identifier:
            raise ValueError("Cannot delete a resource without an identifier.")
        from aiod.calls.calls import delete_asset
        delete_asset(asset_type=self.asset_type, identifier=self.identifier)

    def to_dict(self) -> dict[str, Any]:
        """Convert the resource to a dictionary."""
        d = dataclasses.asdict(self)
        # Remove internal fields or None values if necessary
        return {k: v for k, v in d.items() if v is not None}

    @classmethod
    def _from_dict(cls: type[T], data: dict[str, Any]) -> T:
        """Create a resource instance from a dictionary."""
        # Get the fields of the dataclass
        fields = {f.name for f in dataclasses.fields(cls)}
        # Filter data to only include valid fields
        filtered_data = {k: v for k, v in data.items() if k in fields}
        return cls(**filtered_data)

    def to_pandas(self) -> pd.Series:
        """Convert the resource to a Pandas Series."""
        import pandas as pd
        return pd.Series(self.to_dict())
