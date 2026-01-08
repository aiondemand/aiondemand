# Python Objects (Asset)

The SDK can return lightweight Python objects for assets to improve developer experience.

## Overview

- `Asset`: A thin wrapper around an asset payload allowing attribute-style access and conversion back to a dict via `to_dict()`.
- Opt-in via `data_format='object'` on any resource call that returns a single asset or a list.
- Works alongside existing formats `pandas` (default) and `json`.

## Usage

```python
from aiod.resources import datasets
from aiod.resources.objects import Asset

# Single asset
a = datasets.get_asset("data_...", data_format="object")
assert isinstance(a, Asset)
print(a.identifier)  # convenient attribute
print(a.to_dict()["name"])  # original mapping

# List of assets
items = datasets.get_list(limit=3, data_format="object")
assert all(isinstance(x, Asset) for x in items)
```

## Notes

- `Asset.identifier` is extracted from the payload if available (either top-level or under `aiod_entry`).
- `Asset.asset_type` is annotated from the call context (e.g., `datasets`).

## Other Calls

- Any-asset lookup:

```python
from aiod.calls import calls

a = calls.get_any_asset("data_...", data_format="object")
# -> Asset
```

- Not supported: `get_content(...)` returns raw bytes and does not support `data_format='object'`.

## Async Usage

Async variants also support `data_format='object'` and return `Asset` or `list[Asset]`:

```python
import asyncio
from aiod.resources import datasets
from aiod.resources.objects import Asset

async def main():
	# Multiple identifiers -> list[Asset]
	assets = await datasets.get_assets_async(
		["data_a", "data_b"], data_format="object"
	)
	assert all(isinstance(x, Asset) for x in assets)

	# Batched listing -> list[Asset]
	items = await datasets.get_list_async(limit=5, batch_size=2, data_format="object")
	assert all(isinstance(x, Asset) for x in items)

asyncio.run(main())
```
