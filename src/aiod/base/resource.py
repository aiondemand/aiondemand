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
    def search(
        cls: type[T],
        query: str,
        offset: int = 0,
        limit: int = 100,
        platform: str | None = None,
    ) -> list[T]:
        """Search for resources matching a query."""
        from aiod.calls.calls import search
        platforms = [platform] if platform else None
        data = search(
            query=query,
            asset_type=cls.asset_type,
            offset=offset,
            limit=limit,
            platforms=platforms,
            data_format="json",
        )
        return [cls._from_dict(item) for item in data]

    @classmethod
    def get_from_platform(
        cls: type[T],
        platform: str,
        platform_identifier: str,
    ) -> T:
        """Retrieve a resource by its platform and platform-specific identifier."""
        from aiod.calls.calls import get_asset_from_platform
        data = get_asset_from_platform(
            platform=platform,
            platform_identifier=platform_identifier,
            asset_type=cls.asset_type,
            data_format="json",
        )
        return cls._from_dict(data)

    def get_content(self, distribution_idx: int = 0) -> bytes:
        """Retrieve the data content associated with this resource."""
        if not self.identifier:
            raise ValueError("Resource must have an identifier to fetch content.")
        from aiod.calls.calls import get_content
        return get_content(
            identifier=self.identifier,
            asset_type=self.asset_type,
            distribution_idx=distribution_idx,
        )

    @classmethod
    def counts(cls) -> int | dict[str, int]:
        """Retrieve the number of resources in the metadata catalogue."""
        from aiod.calls.calls import counts
        return counts(asset_type=cls.asset_type)

    def save(self) -> None:
        """Save the resource to the catalogue (register or update)."""
        if self.identifier:
            from aiod.calls.calls import patch_asset
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

    # --- Backward Compatibility Aliases ---
    get_asset = get
    get_list = list
    register = save
    update = save

    def to_dict(self) -> dict[str, Any]:
        """Convert the resource to a dictionary."""
        d = dataclasses.asdict(self)
        return {k: v for k, v in d.items() if v is not None}

    @classmethod
    def _from_dict(cls: type[T], data: dict[str, Any]) -> T:
        """Create a resource instance from a dictionary."""
        fields = {f.name for f in dataclasses.fields(cls)}
        filtered_data = {k: v for k, v in data.items() if k in fields}
        return cls(**filtered_data)

    def to_pandas(self) -> pd.Series:
        """Convert the resource to a Pandas Series."""
        import pandas as pd
        return pd.Series(self.to_dict())
