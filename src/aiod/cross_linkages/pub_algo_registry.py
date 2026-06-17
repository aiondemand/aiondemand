"""Registry mapping publications (DOIs) to AIoD algorithm identifiers.

This registry will be auto-updated by the paper crawling and parsing
pipeline in the future.
"""

from __future__ import annotations

# DOI -> list[class string]
PUB_ALGORITHM_REGISTRY: dict[str, list[str]] = {
    # Paper which introduced Random Forests
    "10.1023/A:1010933404324": [
        "RandomForestClassifier",
    ],
}
