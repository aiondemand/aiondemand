import pytest
import responses
from aiod.resources.datasets import Dataset
from aiod.calls.urls import server_url

@responses.activate
def test_dataset_model_get():
    identifier = "data_1"
    responses.add(
        responses.GET,
        f"{server_url()}v2/datasets/{identifier}",
        json={
            "identifier": identifier,
            "name": "Test Dataset",
            "platform": "zenodo",
            "description": "A test dataset for ESOC"
        },
        status=200
    )
    
    ds = Dataset.get(identifier)
    
    assert isinstance(ds, Dataset)
    assert ds.identifier == identifier
    assert ds.name == "Test Dataset"
    assert ds.platform == "zenodo"
    assert ds.description == "A test dataset for ESOC"

@responses.activate
def test_dataset_model_list():
    responses.add(
        responses.GET,
        f"{server_url()}v2/datasets?offset=0&limit=2",
        json=[
            {"identifier": "1", "name": "DS1"},
            {"identifier": "2", "name": "DS2"}
        ],
        status=200
    )
    
    datasets = Dataset.list(limit=2)
    
    assert len(datasets) == 2
    assert datasets[0].name == "DS1"
    assert datasets[1].name == "DS2"
    assert all(isinstance(d, Dataset) for d in datasets)

def test_dataset_to_dict():
    ds = Dataset(identifier="1", name="Test")
    data = ds.to_dict()
    assert data == {"identifier": "1", "name": "Test"}
    assert "asset_type" not in data

def test_dataset_to_pandas():
    import pandas as pd
    ds = Dataset(identifier="1", name="Test")
    series = ds.to_pandas()
    assert isinstance(series, pd.Series)
    assert series["name"] == "Test"
