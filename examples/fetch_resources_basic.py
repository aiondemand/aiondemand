"""Fetch and display AI resources from the AI-on-Demand metadata catalogue.

This example connects to the AI-on-Demand (AIoD) catalogue using the
``aiondemand`` Python package and prints key metadata for a few datasets.
It is a good starting point if you are new to the package.

Setup
-----
Install the package first:

    pip install aiondemand

Run
---
    python examples/fetch_resources_basic.py
"""

import aiod


def fetch_datasets(limit=5, platform=None):
    """Fetch dataset metadata from the AIoD catalogue.

    Parameters
    ----------
    limit : int
        How many datasets to fetch (default is 5).
    platform : str, optional
        Only fetch datasets from this platform, e.g. "zenodo",
        "openml" or "aida". By default, datasets from all platforms
        are included.

    Returns
    -------
    list of dict
        One dictionary of metadata per dataset.
    """
    datasets = aiod.datasets.get_list(
        platform=platform,
        limit=limit,
        data_format="json",
    )
    return datasets


def display_datasets(datasets):
    """Print key metadata fields for each dataset."""
    for i, item in enumerate(datasets, start=1):
        print(f"Dataset #{i}")
        print(f"  Name       : {item.get('name', 'N/A')}")
        print(f"  Platform   : {item.get('platform', 'N/A')}")
        print(f"  Identifier : {item.get('platform_resource_identifier', 'N/A')}")
        print(f"  Published  : {item.get('date_published', 'N/A')}")
        print("-" * 50)


def main():
    try:
        datasets = fetch_datasets(limit=5)
    except Exception as e:
        print(f"Could not fetch datasets: {e}")
        return
    if not datasets:
        print("No datasets found.")
        return
    display_datasets(datasets)


if __name__ == "__main__":
    main()
