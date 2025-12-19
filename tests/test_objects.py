from http import HTTPStatus

import responses

from aiod.resources import datasets
from aiod.resources.objects import Asset


@responses.activate
def test_get_asset_object_format():
    identifier = "data_abc123"
    payload = {
        "aiod_entry": {"identifier": identifier},
        "name": "Example dataset",
    }
    responses.get(
        f"http://not.set/not_set/datasets/{identifier}",
        json=payload,
        status=HTTPStatus.OK,
    )

    asset = datasets.get_asset(identifier, data_format="object")
    assert isinstance(asset, Asset)
    assert asset.identifier == identifier
    assert asset.asset_type == "datasets"


@responses.activate
def test_get_list_object_format():
    payload = [
        {"aiod_entry": {"identifier": "data_a"}, "name": "A"},
        {"aiod_entry": {"identifier": "data_b"}, "name": "B"},
    ]
    responses.get(
        "http://not.set/not_set/datasets?offset=0&limit=2",
        json=payload,
        status=HTTPStatus.OK,
    )

    assets = datasets.get_list(limit=2, data_format="object")
    assert isinstance(assets, list)
    assert assets and all(isinstance(x, Asset) for x in assets)
    assert all(x.asset_type == "datasets" for x in assets)
