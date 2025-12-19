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
